# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AATNoteSource


class AATNoteSourceInline(TabularInline):
    model = AATNoteSource
    fields = [
        "source_id",
    ]
    readonly_fields = [
        "source_id",
    ]
    verbose_name = "Note Source"
    tab = True
    hide_title = True
    extra = 0
