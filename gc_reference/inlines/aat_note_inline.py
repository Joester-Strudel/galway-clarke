# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AatNote


class AatNoteInline(TabularInline):
    model = AatNote
    fields = [
        "note_text",
    ]
    readonly_fields = [
        "note_text",
    ]
    verbose_name = "Note"
    tab = True
    hide_title = True
    extra = 0
