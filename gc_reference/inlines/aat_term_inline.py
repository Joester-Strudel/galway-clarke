# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AatTerm


class AatTermInline(TabularInline):
    model = AatTerm
    fields = [
        "term_text",
        "display_name",
        "is_preferred",
        "term_type",
    ]
    readonly_fields = [
        "term_text",
        "display_name",
        "is_preferred",
        "term_type",
    ]
    verbose_name = "Term"
    tab = True
    hide_title = True
    extra = 0
