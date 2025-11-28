from django import template

from gc_users.models import GcUser

register = template.Library()


@register.simple_tag
def non_staff_user_count():
    """Return the number of users without staff privileges."""
    return GcUser.objects.filter(is_staff=False).count()
