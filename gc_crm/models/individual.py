# Django Imports
from django.db import models

# Third-Party Imports
from phonenumbers import PhoneNumberFormat, format_number, parse
from phonenumbers.phonenumberutil import NumberParseException

# First-Party Imports
from gc_core.models import SimpleBaseModel


class Individual(SimpleBaseModel):
    # Fields
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="First Name",
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Last Name",
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email",
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Phone",
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
        related_name="crm_individuals_city",
        verbose_name="City",
    )
    location_state = models.ForeignKey(
        "gc_geography.State",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_individuals_state",
        verbose_name="State/Region",
    )
    location_county = models.ForeignKey(
        "gc_geography.County",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_individuals_county",
        verbose_name="County",
    )
    location_zip = models.ForeignKey(
        "gc_geography.ZipCode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_individuals_zip",
        verbose_name="Zip Code",
    )
    organization = models.ForeignKey(
        "gc_crm.Organization",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Organization",
    )
    tags = models.ManyToManyField(
        "gc_crm.Tag",
        blank=True,
        related_name="individuals",
        verbose_name="Tags",
    )
    primary = models.BooleanField(
        default=False,
        verbose_name="Primary Contact",
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes",
        help_text="Internal notes about this individual.",
    )

    # Model Methods
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def full_name(self):
        """Return the full name of the contact."""
        return f"{self.first_name} {self.last_name}"

    def formatted_phone(self):
        try:
            # Change "US" to your default region
            phone_number = parse(self.phone, "US")
            return format_number(phone_number, PhoneNumberFormat.NATIONAL)
        except NumberParseException:
            return self.phone  # Return the original phone if formatting fails

    formatted_phone.short_description = "Phone"

    # Model Metadata
    class Meta:
        verbose_name = "Individual"
        verbose_name_plural = "Individuals"
        ordering = ("-created_at",)
