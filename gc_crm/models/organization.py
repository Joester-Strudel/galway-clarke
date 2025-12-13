# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import HistoryBaseModel


class Organization(HistoryBaseModel):
    """
    CRM organization/account record managed inside the CRM module.
    Separate from gc_users.Team to avoid naming collisions.
    """

    account = models.ForeignKey(
        "gc_users.Team",
        on_delete=models.CASCADE,
        related_name="crm_organizations",
        verbose_name="Team",
        help_text="Owning team within Galway Clarke.",
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Name",
    )
    status = models.ForeignKey(
        "gc_crm.Status",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organizations",
        verbose_name="Status",
        help_text="Lifecycle status for this organization.",
    )
    industry = models.ForeignKey(
        "gc_crm.Industry",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organizations",
        verbose_name="Industry",
    )
    location_city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="City",
    )
    location_state = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="State/Region",
    )
    primary_contact = models.ForeignKey(
        "gc_crm.Individual",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_for_organizations",
        verbose_name="Primary Contact",
    )
    tags = models.ManyToManyField(
        "gc_crm.Tag",
        blank=True,
        related_name="organizations",
        verbose_name="Tags",
        help_text="Labels applied to this organization.",
    )
    last_activity_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Last Activity",
    )

    # Model Methods
    def __str__(self):
        return self.name

    # Model Metadata
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ("name",)
