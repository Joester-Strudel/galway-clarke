# Third-Party Imports
from ninja.security import HttpBearer
from ninja.errors import HttpError
from django.utils.timezone import now
import logging

# First-Party Imports
from gc_users.models import ApiKey, ApiLog


logger = logging.getLogger(__name__)


class GlobalAuth(HttpBearer):
    """
    GlobalAuth enforces API-key authentication on every request, applying:
      1. Existence & activeness checks
      2. Valid date-range checks
      3. Route-permission checks (substring match)
      4. IP-whitelisting (X-Forwarded-For or REMOTE_ADDR)
      5. Detailed logging + JSON errors on failure
    """

    def authenticate(self, request, token):
        """
        Primary authentication entrypoint for Ninja:
          - If the ApiKey doesn’t exist → raise 401 with a JSON message.
          - For each validation step, if it fails → log + raise 403 with a JSON message.
          - If all checks pass → log success, attach api_key to request, and return it.
        """

        # --------------------------
        # 1) Fetch the ApiKey (with prefetch) or fail 401
        # --------------------------
        try:
            api_key = ApiKey.objects.prefetch_related("routes").get(key=token)
        except ApiKey.DoesNotExist:
            request_ip = self._get_request_ip(request)
            logger.warning(
                "GlobalAuth: API key not found; request_ip=%s; path=%s",
                request_ip,
                request.path,
            )
            raise HttpError(401, "Authentication failed: API key does not exist.")

        # --------------------------
        # 2) Run each validation check in sequence
        #    On any failure, log + raise an HttpError(403, message)
        # --------------------------
        for check_fn in (
            self._check_active,
            self._check_date_range,
            self._check_route,
            self._check_ip,
        ):
            passed, message, status_code = check_fn(api_key, request)
            if not passed:
                # Log the failure with full context so you can diagnose in Heroku logs
                request_ip = self._get_request_ip(request)
                permitted_routes = list(api_key.routes.values_list("name", flat=True))
                logger.warning(
                    "GlobalAuth: Check [%s] failed: %s; key_id=%s; "
                    "permitted_routes=%s; request_ip=%s; path=%s",
                    check_fn.__name__,
                    message,
                    api_key.id,
                    permitted_routes,
                    request_ip,
                    request.path,
                )

                # Also insert into your ApiLog table
                self._log_attempt(api_key, message, request, status_code)

                # Now raise a JSON 403 (or 401) so the client sees the exact message
                raise HttpError(status_code, message)

        # --------------------------
        # 3) If all checks passed
        # --------------------------
        # Attach the api_key to the request so downstream code can reference it
        request.api_key = api_key
        return api_key

    def _get_request_ip(self, request):
        """
        Return the “client” IP we’re checking, preferring X-Forwarded-For if present.
        """
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def _check_active(self, api_key, request):
        """
        Return (True, "", 200) if active. Otherwise, (False, message, 403).
        """
        if not api_key.active:
            return (
                False,
                f"Authentication failed: API key '{api_key.name}' is inactive.",
                403,
            )
        return True, "", 200

    def _check_date_range(self, api_key, request):
        """
        Ensure now() is between start_date/end_date.
        Return (False, message, 403) if outside; else (True, "", 200).
        """
        current_time = now()
        if api_key.start_date and api_key.start_date > current_time:
            return (
                False,
                f"Authentication failed: API key '{api_key.name}' not yet valid.",
                403,
            )
        if api_key.end_date and api_key.end_date < current_time:
            return (
                False,
                f"Authentication failed: API key '{api_key.name}' has expired.",
                403,
            )
        return True, "", 200

    def _check_route(self, api_key, request):
        """
        Substring match: if ANY api_key.routes.name is found in request.path, pass.
        If api_key.routes is empty, fail. Otherwise, fail if no match.
        """
        full_path = request.path
        permitted = list(api_key.routes.values_list("name", flat=True))

        if not permitted:
            return (
                False,
                "Authentication failed: No routes permitted for this key.",
                403,
            )

        for route_name in permitted:
            if route_name in full_path:
                return True, "", 200

        return False, "Authentication failed: No permitted route found.", 403

    def _check_ip(self, api_key, request):
        """
        If api_key.ip_address is set, require request_ip == api_key.ip_address.
        Otherwise skip the IP‐check.
        """
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        request_ip = (
            xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")
        )

        if api_key.ip_address and api_key.ip_address != request_ip:
            return False, f"Authentication failed: IP mismatch (got {request_ip}).", 403

        return True, "", 200

    def _log_attempt(self, api_key, message, request, status_code):
        """
        Write a record into your ApiLog table, then emit a Python log line.
        """
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        request_ip = (
            xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")
        )

        ApiLog.objects.create(
            api_key=api_key,
            ip_address=request_ip,
            request_path=request.path,
            status_code=status_code,
            message=message,
        )
