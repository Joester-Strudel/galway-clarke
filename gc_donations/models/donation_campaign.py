# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class DonationCampaign(SimpleBaseModel):
    # Fields
    team = models.ForeignKey(
        "gc_users.Team",
        on_delete=models.CASCADE,
        related_name="donation_campaigns",
        verbose_name="Team",
        help_text="Owning team within Galway Clarke.",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Campaign Name",
        help_text="Public-facing name of the donation campaign.",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Slug",
        help_text="URL-friendly identifier for public donation pages.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Optional description shown on the public donation page.",
    )
    goal_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Goal Amount",
        help_text="Optional fundraising goal for this campaign.",
    )
    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Start Date",
        help_text="Date when this campaign becomes active.",
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="End Date",
        help_text="Optional end date for this campaign.",
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Whether this campaign is currently accepting donations.",
    )
    allow_recurring = models.BooleanField(
        default=False,
        verbose_name="Allow Recurring Donations",
        help_text="Whether donors can make recurring donations to this campaign.",
    )
    suggested_amounts = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Suggested Amounts",
        help_text="Optional list of suggested donation amounts displayed to donors.",
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Internal Notes",
        help_text="Internal notes about this campaign.",
    )

    # Model Methods
    def __str__(self):
        return f"{self.name} ({self.organization})"

    def is_active(self):
        """Return whether the campaign is currently active based on dates and status."""
        if not self.active:
            return False
        if self.start_date and self.start_date > self.created_at.date():
            return False
        if self.end_date and self.end_date < self.created_at.date():
            return False
        return True

    # Model Metadata
    class Meta:
        verbose_name = "Donation Campaign"
        verbose_name_plural = "Donation Campaigns"
        ordering = ("-created_at",)