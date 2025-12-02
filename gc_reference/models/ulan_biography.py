# Django Imports
from django.db import models

# First-Party Imports
from gc_core.models import SimpleBaseModel


class UlanBiography(SimpleBaseModel):
    subject = models.ForeignKey(
        "gc_reference.UlanSubject",
        on_delete=models.CASCADE,
        related_name="biographies",
    )
    biography_id = models.CharField(
        max_length=50,
    )
    biography_text = models.TextField()
    birth_place = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    birth_tgn_id = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    birth_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    death_place = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    death_tgn_id = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    death_date = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    sex = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    contributor_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    is_preferred = models.BooleanField(default=False)

    def __str__(self):
        return self.biography_text[:50]

    class Meta:
        verbose_name = "ULAN Biography"
        verbose_name_plural = "ULAN Biographies"
