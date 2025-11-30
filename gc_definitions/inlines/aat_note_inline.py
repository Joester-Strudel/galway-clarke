# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AATNote


class AATNoteInline(TabularInline):
    model = AATNote
    fields = [
        "note_text",
        "note_language",
    ]
    readonly_fields = [
        "note_text",
        "note_language",
    ]
    verbose_name = "Note"
    tab = True
    hide_title = True
    extra = 0
