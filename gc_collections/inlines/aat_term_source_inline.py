# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AATTermSource


class AATTermSourceInline(TabularInline):
    model = AATTermSource
    fields = [
        "source_id",
        "page",
        "preferred_flag",
    ]
    readonly_fields = [
        "source_id",
        "page",
        "preferred_flag",
    ]
    verbose_name = "Term Source"
    tab = True
    hide_title = True
    extra = 0
