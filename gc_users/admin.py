"""
Admin module that pulls in admin definitions from the dedicated model_admins
package so Django's autodiscovery picks them up.
"""

from django.contrib import admin

admin.site.site_header = "Galway Clarke"
admin.site.site_title = "Galway Clarke"
admin.site.index_title = "Galway Clarke"

# Ensure admin classes are registered
from .model_admins.user_model_admin import GcUserAdmin
