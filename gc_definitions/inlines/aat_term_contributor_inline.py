# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AatTermContributor


class AatTermContributorInline(TabularInline):
    model = AatTermContributor
    fields = [
        "contributor_id",
        "preferred_flag",
    ]
    readonly_fields = [
        "contributor_id",
        "preferred_flag",
    ]
    verbose_name = "Term Contributor"
    tab = True
    hide_title = True
    extra = 0
