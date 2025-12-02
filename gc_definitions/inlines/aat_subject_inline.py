# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AatSubject


class AatSubjectInline(TabularInline):
    model = AatSubject
    fields = [
        "aat_id",
        "record_type",
        "merged_status",
        "sort_order",
        "parent",
        "parent_relationship_type",
    ]
    readonly_fields = [
        "aat_id",
        "record_type",
        "merged_status",
        "sort_order",
        "parent",
        "parent_relationship_type",
    ]
    verbose_name = "Subject"
    tab = True
    hide_title = True
    extra = 0
