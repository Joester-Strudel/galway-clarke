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
