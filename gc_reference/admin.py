# Django Imports
from django.contrib import admin  # noqa: F401
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import path

# First-Party Imports
from . import model_admins  # noqa: F401


def reference_view(request: HttpRequest):
    columns = [
        (
            "AAT",
            [
                ("Subjects", "/admin/gc_reference/aatsubject/"),
                ("Subject Record Types", "/admin/gc_reference/aatsubjectrecordtype/"),
                (
                    "Parent Relationship Types",
                    "/admin/gc_reference/aatparentrelationshiptype/",
                ),
                (
                    "Associative Relationships",
                    "/admin/gc_reference/aatassociativerelationship/",
                ),
                (
                    "Associative Relationship Types",
                    "/admin/gc_reference/aatassociativerelationshiptype/",
                ),
                ("Terms", "/admin/gc_reference/aatterm/"),
                ("Term Contributors", "/admin/gc_reference/aattermcontributor/"),
                ("Term Sources", "/admin/gc_reference/aattermsource/"),
                ("Notes", "/admin/gc_reference/aatnote/"),
                ("Note Contributors", "/admin/gc_reference/aatnotecontributor/"),
                ("Note Sources", "/admin/gc_reference/aatnotesource/"),
                ("Subject Contributors", "/admin/gc_reference/aatsubjectcontributor/"),
                ("Subject Sources", "/admin/gc_reference/aatsubjectsource/"),
            ],
        ),
        (
            "ULAN",
            [
                ("Subjects", "/admin/gc_reference/ulansubject/"),
                ("Subject Record Types", "/admin/gc_reference/ulansubjectrecordtype/"),
                (
                    "Parent Relationship Types",
                    "/admin/gc_reference/ulanparentrelationshiptype/",
                ),
                (
                    "Associative Relationships",
                    "/admin/gc_reference/ulanassociativerelationship/",
                ),
                (
                    "Associative Relationship Types",
                    "/admin/gc_reference/ulanassociativerelationshiptype/",
                ),
                ("Terms", "/admin/gc_reference/ulanterm/"),
                ("Term Types", "/admin/gc_reference/ulantermtype/"),
                ("Parts of Speech", "/admin/gc_reference/ulanpartofspeech/"),
                ("Term Contributors", "/admin/gc_reference/ulantermcontributor/"),
                ("Term Sources", "/admin/gc_reference/ulantermsource/"),
                ("Notes", "/admin/gc_reference/ulannote/"),
                ("Note Contributors", "/admin/gc_reference/ulannotecontributor/"),
                ("Note Sources", "/admin/gc_reference/ulannotesource/"),
                ("Subject Contributors", "/admin/gc_reference/ulansubjectcontributor/"),
                ("Subject Sources", "/admin/gc_reference/ulansubjectsource/"),
                ("Biographies", "/admin/gc_reference/ulanbiography/"),
                ("Roles", "/admin/gc_reference/ulanrole/"),
                ("Nationalities", "/admin/gc_reference/ulannationality/"),
            ],
        ),
        (
            "Languages",
            [
                ("ISO Languages", "/admin/gc_reference/isolanguage/"),
                ("ISO Language Scopes", "/admin/gc_reference/isolanguagescope/"),
                ("ISO Language Types", "/admin/gc_reference/isolanguagetype/"),
            ],
        ),
    ]
    context = admin.site.each_context(request)
    context.update({"page_title": "Reference Dashboard", "columns": columns})
    return TemplateResponse(request, "admin/reference.html", context)


def aat_view(request: HttpRequest):
    links = [
        ("Subjects", "/admin/gc_reference/aatsubject/"),
        ("Subject Record Types", "/admin/gc_reference/aatsubjectrecordtype/"),
        ("Parent Relationship Types", "/admin/gc_reference/aatparentrelationshiptype/"),
        (
            "Associative Relationships",
            "/admin/gc_reference/aatassociativerelationship/",
        ),
        (
            "Associative Relationship Types",
            "/admin/gc_reference/aatassociativerelationshiptype/",
        ),
        ("Terms", "/admin/gc_reference/aatterm/"),
        ("Term Contributors", "/admin/gc_reference/aattermcontributor/"),
        ("Term Sources", "/admin/gc_reference/aattermsource/"),
        ("Notes", "/admin/gc_reference/aatnote/"),
        ("Note Contributors", "/admin/gc_reference/aatnotecontributor/"),
        ("Note Sources", "/admin/gc_reference/aatnotesource/"),
        ("Subject Contributors", "/admin/gc_reference/aatsubjectcontributor/"),
        ("Subject Sources", "/admin/gc_reference/aatsubjectsource/"),
    ]
    return _render_dashboard(
        request,
        template_name="admin/aat_dashboard.html",
        title="AAT Dashboard",
        links=links,
    )


def ulan_view(request: HttpRequest):
    links = [
        ("Subjects", "/admin/gc_reference/ulansubject/"),
        ("Subject Record Types", "/admin/gc_reference/ulansubjectrecordtype/"),
        (
            "Parent Relationship Types",
            "/admin/gc_reference/ulanparentrelationshiptype/",
        ),
        (
            "Associative Relationships",
            "/admin/gc_reference/ulanassociativerelationship/",
        ),
        (
            "Associative Relationship Types",
            "/admin/gc_reference/ulanassociativerelationshiptype/",
        ),
        ("Terms", "/admin/gc_reference/ulanterm/"),
        ("Term Types", "/admin/gc_reference/ulantermtype/"),
        ("Parts of Speech", "/admin/gc_reference/ulanpartofspeech/"),
        ("Term Contributors", "/admin/gc_reference/ulantermcontributor/"),
        ("Term Sources", "/admin/gc_reference/ulantermsource/"),
        ("Notes", "/admin/gc_reference/ulannote/"),
        ("Note Contributors", "/admin/gc_reference/ulannotecontributor/"),
        ("Note Sources", "/admin/gc_reference/ulannotesource/"),
        ("Subject Contributors", "/admin/gc_reference/ulansubjectcontributor/"),
        ("Subject Sources", "/admin/gc_reference/ulansubjectsource/"),
        ("Biographies", "/admin/gc_reference/ulanbiography/"),
        ("Roles", "/admin/gc_reference/ulanrole/"),
        ("Nationalities", "/admin/gc_reference/ulannationality/"),
    ]
    return _render_dashboard(
        request,
        template_name="admin/ulan_dashboard.html",
        title="ULAN Dashboard",
        links=links,
    )


def languages_view(request: HttpRequest):
    links = [
        ("ISO Languages", "/admin/gc_reference/isolanguage/"),
        ("ISO Language Scopes", "/admin/gc_reference/isolanguagescope/"),
        ("ISO Language Types", "/admin/gc_reference/isolanguagetype/"),
    ]
    return _render_dashboard(
        request,
        template_name="admin/languages_dashboard.html",
        title="Languages Dashboard",
        links=links,
    )


def _render_dashboard(request: HttpRequest, template_name: str, title: str, links):
    context = admin.site.each_context(request)
    context.update({"page_title": title, "links": links})
    return TemplateResponse(request, template_name, context)


# Preserve the original get_urls so we don't recurse
_original_get_urls = admin.site.get_urls


def get_urls():
    urls = _original_get_urls()
    custom_urls = [
        path("reference/", admin.site.admin_view(reference_view), name="reference"),
        path("aat/", admin.site.admin_view(aat_view), name="aat"),
        path("ulan/", admin.site.admin_view(ulan_view), name="ulan"),
        path("languages/", admin.site.admin_view(languages_view), name="languages"),
    ]
    return custom_urls + urls


admin.site.get_urls = get_urls
