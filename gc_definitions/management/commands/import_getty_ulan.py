import os
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from gc_definitions.models import (
    IsoLanguage,
    UlanSubject,
    UlanSubjectContributor,
    UlanSubjectSource,
    UlanNote,
    UlanNoteContributor,
    UlanNoteSource,
    UlanTerm,
    UlanTermContributor,
    UlanTermSource,
    UlanAssociativeRelationship,
    UlanBiography,
    UlanRole,
    UlanNationality,
)


ULAN_FOLDER = os.path.join(
    settings.BASE_DIR,
    "data",
    "vocabularies",
    "GattyULAN",
)


class Command(BaseCommand):
    help = "Import all Getty ULAN XML files into the database."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting ULAN import…"))
        xml_files = sorted(
            f for f in os.listdir(ULAN_FOLDER) if f.endswith(".xml")
        )

        if not xml_files:
            self.stdout.write(self.style.WARNING("No XML files found."))
            return

        for filename in xml_files:
            full_path = os.path.join(ULAN_FOLDER, filename)
            try:
                self.import_single_file(full_path)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error importing {filename}: {e}")
                )

        self.stdout.write(self.style.SUCCESS("ULAN import complete."))

    # -------------------------------------------------------------

    @transaction.atomic
    def import_single_file(self, filepath: str):
        tree = ET.parse(filepath)
        root = tree.getroot()
        subject_el = root.find("Subject")

        if subject_el is None:
            self.stdout.write(self.style.WARNING(f"No <Subject> in {filepath}"))
            return

        ulan_id = subject_el.attrib.get("Subject_ID")

        subject, _ = UlanSubject.objects.get_or_create(
            ulan_id=ulan_id,
        )

        # ---------------------------------------------------------
        # BASIC SUBJECT FIELDS
        # ---------------------------------------------------------
        subject.record_type = self._text(subject_el, "Record_Type")
        subject.merged_status = self._text(subject_el, "Merged_Status")

        # Parent Relationships
        parent_el = subject_el.find("Parent_Relationships/Preferred_Parent")
        if parent_el is not None:
            subject.parent_ulan_id = self._text(parent_el, "Parent_Subject_ID")
            subject.parent_string = self._text(parent_el, "Parent_String")
            subject.parent_relationship_type = self._text(parent_el, "Hier_Rel_Type")
            subject.parent_historic_flag = self._text(parent_el, "Historic_Flag")

        subject.save()

        # ---------------------------------------------------------
        # TERMS
        # ---------------------------------------------------------
        self._import_terms(subject, subject_el.find("Terms"))

        # ---------------------------------------------------------
        # ASSOCIATIVE RELATIONSHIPS
        # ---------------------------------------------------------
        self._import_associative_relationships(subject, subject_el.find("Associative_Relationships"))

        # ---------------------------------------------------------
        # SUBJECT CONTRIBUTORS
        # ---------------------------------------------------------
        self._import_subject_contributors(subject, subject_el.find("Subject_Contributors"))

        # ---------------------------------------------------------
        # SUBJECT SOURCES
        # ---------------------------------------------------------
        self._import_subject_sources(subject, subject_el.find("Subject_Sources"))

        # ---------------------------------------------------------
        # BIOGRAPHIES
        # ---------------------------------------------------------
        self._import_biographies(subject, subject_el.find("Biographies"))

        # ---------------------------------------------------------
        # ROLES
        # ---------------------------------------------------------
        self._import_roles(subject, subject_el.find("Roles"))

        # ---------------------------------------------------------
        # NATIONALITIES
        # ---------------------------------------------------------
        self._import_nationalities(subject, subject_el.find("Nationalities"))

        self.stdout.write(self.style.SUCCESS(f"Imported {ulan_id}"))

    # ===================================================================
    # HELPERS
    # ===================================================================

    def _text(self, parent, tag):
        """Safe helper to get the text of a tag or None."""
        if parent is None:
            return None
        el = parent.find(tag)
        return el.text.strip() if el is not None and el.text else None

    def _get_language(self, lang_text):
        """
        Convert something like '70001/undetermined' into an IsoLanguage.
        """
        if not lang_text:
            return None

        code = lang_text.split("/")[0]  # "70001"
        name = lang_text.split("/", 1)[1] if "/" in lang_text else None

        lang, _ = IsoLanguage.objects.get_or_create(
            getty_language_code=code,
            defaults={"name": name or code},
        )
        return lang

    # ===================================================================
    # IMPORT BLOCKS
    # ===================================================================

    def _import_terms(self, subject, terms_el):
        if terms_el is None:
            return

        for term_block in list(terms_el):
            is_preferred = term_block.tag == "Preferred_Term"

            term_id = self._text(term_block, "Term_ID")
            term_text = self._text(term_block, "Term_Text")

            if term_id is None:
                continue

            term, _ = UlanTerm.objects.get_or_create(
                subject=subject,
                term_id=term_id,
                defaults={"term_text": term_text},
            )

            term.term_text = term_text
            term.display_name = self._text(term_block, "Display_Name")
            term.historic_flag = self._text(term_block, "Historic_Flag")
            term.vernacular = self._text(term_block, "Vernacular")
            term.is_preferred = is_preferred

            # Single-language per term in ULAN
            lang_block = term_block.find("Term_Languages/Term_Language")
            if lang_block is not None:
                raw_lang = self._text(lang_block, "Language")
                term.language_code = self._get_language(raw_lang)
                term.term_type = self._text(lang_block, "Term_Type")
                term.part_of_speech = self._text(lang_block, "Part_of_Speech")
                term.qualifier = self._text(lang_block, "Qualifier")

            term.save()

            # Contributors
            contribs = term_block.find("Term_Contributors")
            if contribs is not None:
                for c in contribs.findall("Term_Contributor"):
                    cid = self._text(c, "Contributor_id")
                    if cid:
                        UlanTermContributor.objects.get_or_create(
                            term=term,
                            contributor_id=cid,
                            preferred_flag=self._text(c, "Preferred"),
                        )

            # Sources
            sources = term_block.find("Term_Sources")
            if sources is not None:
                for s in sources.findall("Term_Source"):
                    src_id = self._text(s.find("Source"), "Source_ID")
                    if src_id:
                        UlanTermSource.objects.get_or_create(
                            term=term,
                            source_id=src_id,
                            page=self._text(s, "Page"),
                            preferred_flag=self._text(s, "Preferred"),
                        )

    def _import_associative_relationships(self, subject, ar_el):
        if ar_el is None:
            return

        for block in ar_el.findall("Associative_Relationship"):
            rel_type = self._text(block, "Relationship_Type")
            vp_id = self._text(block.find("Related_Subject_ID"), "VP_Subject_ID")

            ar, _ = UlanAssociativeRelationship.objects.get_or_create(
                subject=subject,
                relationship_type=rel_type,
                related_ulan_id=vp_id,
            )

            ar.historic_flag = self._text(block, "Historic_Flag")

            # Optional AR dates
            date_el = block.find("AR_Date")
            if date_el is not None:
                ar.display_date = self._text(date_el, "Display_Date")
                ar.start_date = self._text(date_el, "Start_Date")
                ar.end_date = self._text(date_el, "End_Date")

            ar.save()

    def _import_subject_contributors(self, subject, contrib_el):
        if contrib_el is None:
            return
        for c in contrib_el.findall("Subject_Contributor"):
            cid = self._text(c, "Contributor_id")
            if cid:
                UlanSubjectContributor.objects.get_or_create(
                    subject=subject,
                    contributor_id=cid,
                )

    def _import_subject_sources(self, subject, sources_el):
        if sources_el is None:
            return
        for s in sources_el.findall("Subject_Source"):
            src_id = self._text(s.find("Source"), "Source_ID")
            if src_id:
                UlanSubjectSource.objects.get_or_create(
                    subject=subject,
                    source_id=src_id,
                )

    def _import_biographies(self, subject, bios_el):
        if bios_el is None:
            return

        for block in list(bios_el):
            bio_id = self._text(block, "Biography_ID")
            if not bio_id:
                continue

            bio, _ = UlanBiography.objects.get_or_create(
                subject=subject,
                biography_id=bio_id,
            )

            bio.biography_text = self._text(block, "Biography_Text")
            bio.birth_place = self._text(block, "Birth_Place")
            bio.birth_date = self._text(block, "Birth_Date")
            bio.birth_tgn_id = self._text(block, "Birth_TGN_ID")
            bio.death_place = self._text(block, "Death_Place")
            bio.death_date = self._text(block, "Death_Date")
            bio.death_tgn_id = self._text(block, "Death_TGN_ID")
            bio.sex = self._text(block, "Sex")
            bio.contributor_id = self._text(block, "Contributor")
            bio.is_preferred = "Preferred" in block.tag

            bio.save()

    def _import_roles(self, subject, roles_el):
        if roles_el is None:
            return

        for block in list(roles_el):
            role_id = self._text(block, "Role_ID")
            if not role_id:
                continue

            role, _ = UlanRole.objects.get_or_create(
                subject=subject,
                role_id=role_id,
            )
            role.historic_flag = self._text(block, "Historic_Flag")
            role.is_preferred = "Preferred" in block.tag
            role.save()

    def _import_nationalities(self, subject, nat_el):
        if nat_el is None:
            return

        for block in list(nat_el):
            nat_code = self._text(block, "Nationality_Code")
            if not nat_code:
                continue

            nat, _ = UlanNationality.objects.get_or_create(
                subject=subject,
                nationality_code=nat_code,
            )
            nat.display_order = self._text(block, "Display_Order")
            nat.is_preferred = "Preferred" in block.tag
            nat.save()