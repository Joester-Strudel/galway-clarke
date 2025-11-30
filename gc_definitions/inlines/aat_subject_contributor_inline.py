# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import AATSubjectContributor


class AATSubjectContributorInline(TabularInline):
    model = AATSubjectContributor
    fields = [
        "contributor_id",
    ]
    readonly_fields = [
        "contributor_id",
    ]
    verbose_name = "Subject Contributor"
    tab = True
    hide_title = True
    extra = 0
