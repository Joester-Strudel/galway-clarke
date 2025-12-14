# Django Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from gc_crm.views.organizations_view import _get_org_page, _pagination_context


@login_required
def index_view(request):
    """
    Redirect to organizations as the default CRM tab.
    """
    return redirect(reverse("crm-organizations"))
