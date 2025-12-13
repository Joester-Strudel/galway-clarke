# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class Industry(SimpleBaseModel):
    # Fields
    team = models.ForeignKey(
        "gc_users.Team",
        on_delete=models.CASCADE,
        related_name="crm_industries",
        verbose_name="Team",
        help_text="Team that owns this industry definition.",
    )
    name = models.CharField(
        max_length=120,
        blank=False,
        null=False,
        verbose_name="Name",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )

    # Model Methods
    def __str__(self):
        return self.name

    # Model Metadata
    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        ordering = ("name",)
