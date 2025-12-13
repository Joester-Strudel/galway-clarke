# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class Tag(SimpleBaseModel):
    # Fields
    team = models.ForeignKey(
        "gc_users.Team",
        on_delete=models.CASCADE,
        related_name="crm_tags",
        verbose_name="Team",
        help_text="Team that owns this tag.",
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="Name",
    )
    color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Color",
        help_text="Optional hex or token to style this tag.",
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
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ("name",)
