# Third-Party Imports
from unfold.admin import TabularInline

# First-Party Imports
from ..models import Collection


class CollectionInline(TabularInline):
    model = Collection
    fields = [
        "name",
        "organization",
    ]
    readonly_fields = [
        "name",
        "organization",
    ]
    verbose_name = "Collection"
    tab = True
    hide_title = True
    extra = 0
