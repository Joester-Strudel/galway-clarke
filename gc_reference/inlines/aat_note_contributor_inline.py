# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AatNoteContributor


class AatNoteContributorInline(TabularInline):
    model = AatNoteContributor
    fields = [
        "contributor_id",
    ]
    readonly_fields = [
        "contributor_id",
    ]
    verbose_name = "Note Contributor"
    tab = True
    hide_title = True
    extra = 0
