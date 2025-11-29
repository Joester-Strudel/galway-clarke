# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AATAssociativeRelationship


class AATAssociativeRelationshipInline(TabularInline):
    model = AATAssociativeRelationship
    fields = [
        "relationship_type",
        "related_aat_id",
        "historic_flag",
    ]
    readonly_fields = [
        "relationship_type",
        "related_aat_id",
        "historic_flag",
    ]
    verbose_name = "Associative Relationship"
    tab = True
    hide_title = True
    extra = 0
