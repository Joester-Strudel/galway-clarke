# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models.simple_base_model import SimpleBaseModel


class ApiLog(SimpleBaseModel):
    api_key = models.ForeignKey(
        "gc_users.ApiKey",
        on_delete=models.CASCADE,
        related_name="api_logs",
        related_query_name="api_log",
        null=True,
        blank=True,
        verbose_name="API Key",
        help_text="The API key used to make this call.",
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        protocol="both",
        unpack_ipv4=True,
        verbose_name="IP Address",
        help_text="The IP address of the request sender.",
    )
    request_path = models.CharField(
        max_length=2048,
        null=True,
        blank=True,
        verbose_name="Request Path",
        help_text="The API request path (e.g., '/api/orders/123/').",
    )
    status_code = models.IntegerField(
        null=True,
        blank=True,
        choices=[
            (200, "OK"),
            (201, "Created"),
            (204, "No Content"),
            (400, "Bad Request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not Found"),
            (500, "Internal Server Error"),
            (502, "Bad Gateway"),
            (503, "Service Unavailable"),
        ],
        verbose_name="Status Code",
        help_text="HTTP status code returned by the API call.",
    )
    message = models.TextField(
        null=True,
        blank=True,
        default="",
        verbose_name="Message",
        help_text="System-generated message describing the request result.",
    )

    class Meta:
        verbose_name = "API Log Entry"
        verbose_name_plural = "API Log Entries"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["api_key"]),
            models.Index(fields=["status_code"]),
        ]

    def __str__(self):
        return f"API Log ({self.created_at}) - {self.api_key.name if self.api_key else 'No API Key'}"
