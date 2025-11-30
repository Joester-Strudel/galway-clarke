# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AATTerm


class AATTermInline(TabularInline):
    model = AATTerm
    fields = [
        "term_text",
        "display_name",
        "is_preferred",
        "term_type",
        "language_code",
    ]
    readonly_fields = [
        "term_text",
        "display_name",
        "is_preferred",
        "term_type",
        "language_code",
    ]
    verbose_name = "Term"
    tab = True
    hide_title = True
    extra = 0
