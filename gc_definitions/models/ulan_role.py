# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanRole(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_definitions.UlanSubject",
        on_delete=models.CASCADE,
        related_name="roles",
    )
    role_id = models.CharField(
        max_length=100,
    )
    historic_flag = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    is_preferred = models.BooleanField(default=False,)

    def __str__(self):
        return self.role_id

    class Meta:
        verbose_name = "ULAN Role"
        verbose_name_plural = "ULAN Roles"