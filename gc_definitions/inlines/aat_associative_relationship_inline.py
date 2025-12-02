# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AatAssociativeRelationship


class AatAssociativeRelationshipInline(TabularInline):
    model = AatAssociativeRelationship
    fields = [
        "relationship_type",
        "related_subject",
        "historic_flag",
    ]
    readonly_fields = [
        "relationship_type",
        "related_subject",
        "historic_flag",
    ]
    verbose_name = "Associative Relationship"
    tab = True
    hide_title = True
    extra = 0
