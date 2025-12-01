# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AatSubjectSource


class AatSubjectSourceInline(TabularInline):
    model = AatSubjectSource
    fields = [
        "source_id",
    ]
    readonly_fields = [
        "source_id",
    ]
    verbose_name = "Subject Source"
    tab = True
    hide_title = True
    extra = 0
