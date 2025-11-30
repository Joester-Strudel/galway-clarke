# Python Imports
import os
import glob
import xml.etree.ElementTree as ET

# Django Imports
from django.core.management.base import BaseCommand
from django.db import transaction

# First-Party Imports
from gc_definitions.models import (
    AATSubject,
    AATSubjectContributor,
    AATSubjectSource,
    AATAssociativeRelationship,
    AATNote,
    AATNoteContributor,
    AATNoteSource,
    AATTerm,
    AATTermContributor,
    AATTermSource,
)


def clean(value):
    if value is None:
        return None
    value = value.strip()
    return value if value else None


class Command(BaseCommand):
    help = "Import Getty AAT XML files into the vocabulary models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default="data/vocabularies/GettyAAT/",
            help="Directory containing AAT XML files",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        base_path = options["path"]

        xml_files = glob.glob(os.path.join(base_path, "*.xml"))
        xml_files = xml_files[:50]  # Limit processing to first 50 entries
        total = len(xml_files)

        self.stdout.write(f"Found {total} AAT XML files...")

        for idx, xml_path in enumerate(xml_files, start=1):
            self.stdout.write(
                f"-- [{idx}/{total}] Importing {os.path.basename(xml_path)}"
            )

            tree = ET.parse(xml_path)
            root = tree.getroot()

            subject_el = root.find("Subject")
            subject_id = subject_el.get("Subject_ID")

            # ---------------------------------------------------------
            # FIXED FIELD NAME: uses aat_id instead of subject_id
            # ---------------------------------------------------------
            subject, _ = AATSubject.objects.get_or_create(
                aat_id=subject_id,
            )

            # ---------------------------------------------------------
            # Preferred Parent
            # ---------------------------------------------------------
            parent_rel = subject_el.find("Parent_Relationships/Preferred_Parent")
            if parent_rel is not None:
                subject.parent_aat_id = clean(parent_rel.findtext("Parent_Subject_ID"))
                subject.parent_relationship_type = clean(
                    parent_rel.findtext("Relationship_Type")
                )
                subject.parent_historic_flag = clean(
                    parent_rel.findtext("Historic_Flag")
                )
                subject.parent_string = clean(parent_rel.findtext("Parent_String"))
                subject.hier_rel_type = clean(parent_rel.findtext("Hier_Rel_Type"))

            # ---------------------------------------------------------
            # Subject-level metadata
            # ---------------------------------------------------------
            subject.record_type = clean(subject_el.findtext("Record_Type"))
            subject.merged_status = clean(subject_el.findtext("Merged_Status"))
            subject.sort_order = clean(subject_el.findtext("Sort_Order"))
            subject.save()

            # ---------------------------------------------------------
            # Subject Contributors
            # ---------------------------------------------------------
            for contrib_el in subject_el.findall(
                "Subject_Contributors/Subject_Contributor"
            ):
                cid = clean(contrib_el.findtext("Contributor_id"))
                if cid:
                    AATSubjectContributor.objects.get_or_create(
                        subject=subject,
                        contributor_id=cid,
                    )

            # ---------------------------------------------------------
            # Subject Sources
            # ---------------------------------------------------------
            for src_el in subject_el.findall("Subject_Sources/Subject_Source/Source"):
                sid = clean(src_el.findtext("Source_ID"))
                if sid:
                    AATSubjectSource.objects.get_or_create(
                        subject=subject,
                        source_id=sid,
                    )

            # ---------------------------------------------------------
            # Descriptive Notes
            # ---------------------------------------------------------
            for note_el in subject_el.findall("Descriptive_Notes/Descriptive_Note"):
                note = AATNote.objects.create(
                    subject=subject,
                    note_text=clean(note_el.findtext("Note_Text")),
                    note_language=clean(note_el.findtext("Note_Language")),
                )

                # ---- Note Contributors ----
                for nc_el in note_el.findall("Note_Contributors/Note_Contributor"):
                    cid = clean(nc_el.findtext("Contributor_id"))
                    if cid:
                        AATNoteContributor.objects.create(
                            note=note,
                            contributor_id=cid,
                        )

                # ---- Note Sources ----
                for ns_el in note_el.findall("Note_Sources/Note_Source/Source"):
                    sid = clean(ns_el.findtext("Source_ID"))
                    if sid:
                        AATNoteSource.objects.create(
                            note=note,
                            source_id=sid,
                        )

            # ---------------------------------------------------------
            # Terms (Preferred + Non Preferred)
            # ---------------------------------------------------------
            terms_el = subject_el.find("Terms")
            if terms_el is not None:
                for term_el in terms_el:
                    term_text = clean(term_el.findtext("Term_Text"))
                    if not term_text:
                        continue

                    term = AATTerm.objects.create(
                        subject=subject,
                        term_id=clean(term_el.findtext("Term_ID")),
                        term_text=term_text,
                        display_name=clean(term_el.findtext("Display_Name")),
                        historic_flag=clean(term_el.findtext("Historic_Flag")),
                        vernacular=clean(term_el.findtext("Vernacular")),
                        is_preferred=(term_el.tag == "Preferred_Term"),
                    )

                    # ---- Term Languages ----
                    for lang_el in term_el.findall("Term_Languages/Term_Language"):
                        language_code_raw = clean(lang_el.findtext("Language"))
                        term.language_code = language_code_raw

                        term.term_type = clean(lang_el.findtext("Term_Type"))
                        term.part_of_speech = clean(lang_el.findtext("Part_of_Speech"))
                        term.qualifier = clean(lang_el.findtext("Qualifier"))
                        term.save()

                    # ---- Term Contributors ----
                    for tcon_el in term_el.findall(
                        "Term_Contributors/Term_Contributor"
                    ):
                        cid = clean(tcon_el.findtext("Contributor_id"))
                        if cid:
                            AATTermContributor.objects.create(
                                term=term,
                                contributor_id=cid,
                                preferred_flag=clean(tcon_el.findtext("Preferred")),
                            )

                    # ---- Term Sources ----
                    for ts_el in term_el.findall("Term_Sources/Term_Source"):
                        src_el = ts_el.find("Source")
                        if src_el is not None:
                            sid = clean(src_el.findtext("Source_ID"))
                            if sid:
                                AATTermSource.objects.create(
                                    term=term,
                                    source_id=sid,
                                    page=clean(ts_el.findtext("Page")),
                                    preferred_flag=clean(ts_el.findtext("Preferred")),
                                )

            # ---------------------------------------------------------
            # Associative Relationships
            # ---------------------------------------------------------
            assoc_parent = subject_el.find("Associative_Relationships")
            if assoc_parent is not None:
                for ar in assoc_parent.findall("Associative_Relationship"):
                    AATAssociativeRelationship.objects.create(
                        subject=subject,
                        relationship_type=clean(ar.findtext("Relationship_Type")),
                        related_aat_id=clean(
                            ar.findtext("Related_Subject_ID/VP_Subject_ID")
                        ),
                        historic_flag=clean(ar.findtext("Historic_Flag")),
                    )

        self.stdout.write(self.style.SUCCESS("AAT import completed successfully."))
