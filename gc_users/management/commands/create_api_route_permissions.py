"""
Create ApiRoute records for every discovered API URL under /api/.

This walks the Django URL resolver directly (instead of relying on external
commands like `show_urls`), normalizes each /api/ path by stripping dynamic
parameters, collapsing duplicate slashes, and enforcing a trailing slash, then
creates missing ApiRoute rows.
"""

# Python Imports
import re

# Third-Party Imports
from django.core.management.base import BaseCommand
from django.urls import URLPattern, URLResolver, get_resolver

# First-Party Imports
from ...models import ApiRoute


class Command(BaseCommand):
    help = (
        "Lists all API URLs (starting with '/api/'), removes dynamic parameters, "
        "collapses any duplicate slashes, ensures they end with exactly one '/', "
        "and creates or gets ApiRoute objects."
    )

    def handle(self, *args, **options):
        urls = self._gather_api_urls()

        route_counts = {}

        for raw_path in urls:
            # 1. Remove anything inside '<…>' (dynamic URL parameters)
            cleaned_url = re.sub(r"<[^>]+>", "", raw_path)

            # 2. Collapse any duplicate slashes ('//' → '/', '///' → '/', etc.)
            cleaned_url = re.sub(r"/{2,}", "/", cleaned_url)

            # 3. Ensure exactly one trailing slash
            if not cleaned_url.endswith("/"):
                cleaned_url += "/"

            route_counts[cleaned_url] = route_counts.get(cleaned_url, 0) + 1

            api_route, created = ApiRoute.objects.get_or_create(name=cleaned_url)

            if created:
                self.stdout.write(f"Created: {api_route.name}")
            else:
                self.stdout.write(f"Already exists: {api_route.name}")

        duplicates = [route for route, count in route_counts.items() if count > 1]
        if duplicates:
            self.stdout.write(self.style.WARNING("\nDuplicate routes detected:"))
            for route in duplicates:
                self.stdout.write(
                    self.style.WARNING(f"{route} (appears {route_counts[route]} times)")
                )
        else:
            self.stdout.write(self.style.SUCCESS("\nNo duplicate routes detected."))

    def _gather_api_urls(self):
        """Traverse the URL resolver and return all paths that start with /api/."""
        resolver = get_resolver()
        paths = []

        def walk(patterns, prefix=""):
            for pattern in patterns:
                if isinstance(pattern, URLPattern):
                    route = prefix + str(pattern.pattern)
                    if route.startswith("api/") or route.startswith("/api/"):
                        paths.append("/" + route.lstrip("/"))
                elif isinstance(pattern, URLResolver):
                    walk(pattern.url_patterns, prefix + str(pattern.pattern))

        walk(resolver.url_patterns)
        return paths
