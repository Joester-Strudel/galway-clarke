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
    address_one = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Address Line 1",
    )
    address_two = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Address Line 2",
    )
    location_city = models.ForeignKey(
        "gc_geography.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_organizations",
        verbose_name="City",
    )
    location_state = models.ForeignKey(
        "gc_geography.State",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_organizations",
        verbose_name="State/Region",
    )
    location_county = models.ForeignKey(
        "gc_geography.County",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_organizations",
        verbose_name="County",
    )
    location_zip = models.ForeignKey(
        "gc_geography.ZipCode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_organizations",
        verbose_name="Zip Code",
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
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes",
        help_text="Internal notes about this organization.",
    )

    # Model Methods
    def __str__(self):
        return self.name

    # Model Metadata
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ("name",)
