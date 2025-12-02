# Python Imports
import re
import time
from urllib.parse import urljoin

# Django Imports
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Third-Party Imports
import requests
from bs4 import BeautifulSoup

# First-Party Imports
from gc_reference.models import IsoLanguage, IsoLanguageScope, IsoLanguageType


class Command(BaseCommand):
    help = "Scrape ISO 639 data from iso639-3.sil.org and create/update ISO language records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            default="https://iso639-3.sil.org/code_tables/639/data/all",
            help="Base URL for the ISO 639 data table.",
        )

    def handle(self, *args, **options):
        base_url = options["url"]
        seen_pages = set()
        current_url = base_url
        created = 0
        updated = 0
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

        while current_url and current_url not in seen_pages:
            seen_pages.add(current_url)
            self.stdout.write(f"Fetching {current_url}")

            response = self._fetch_with_retry(session, current_url, timeout=30)
            if response.status_code != 200:
                raise CommandError(
                    f"Failed to fetch {current_url} (status {response.status_code})"
                )

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            if table is None:
                raise CommandError(f"No table found at {current_url}")

            headers = [
                self._normalize_header(th.get_text()) for th in table.find_all("th")
            ]
            rows = table.find_all("tr")

            with transaction.atomic():
                for row in rows:
                    cells = row.find_all("td")
                    if not cells:
                        continue  # skip header or malformed rows

                    data = [cell.get_text(strip=True) for cell in cells]
                    iso3 = self._get_column_value(
                        headers, data, ["id", "639-3", "639 3", "iso639-3"]
                    )
                    if not iso3:
                        continue

                    name = self._get_column_value(
                        headers,
                        data,
                        [
                            "language name(s)",
                            "language name",
                            "ref name",
                            "reference name",
                            "name",
                        ],
                    )
                    iso1 = self._get_column_value(headers, data, ["639-1", "iso639-1"])
                    combined_2_5 = self._get_column_value(
                        headers, data, ["639-2/639-5", "639-2 / 639-5", "639-2 639-5"]
                    )
                    scope_value = self._get_column_value(headers, data, ["scope"])
                    type_value = self._get_column_value(
                        headers, data, ["type", "language type"]
                    )

                    iso2, iso5 = self._parse_iso2_iso5(combined_2_5)

                    scope_obj = None
                    type_obj = None
                    if scope_value:
                        scope_obj, _ = IsoLanguageScope.objects.get_or_create(
                            name=scope_value
                        )
                    if type_value:
                        type_obj, _ = IsoLanguageType.objects.get_or_create(
                            name=type_value
                        )

                    obj, created_flag = IsoLanguage.objects.update_or_create(
                        iso_set_639_3_code=iso3,
                        defaults={
                            "name": name or iso3,
                            "iso_set_639_1_code": iso1 or None,
                            "iso_set_639_2_code": iso2,
                            "iso_set_639_5_code": iso5,
                            "iso_language_scope": scope_obj,
                            "iso_language_type": type_obj,
                        },
                    )

                    if created_flag:
                        created += 1
                    else:
                        updated += 1

            next_url = self._find_next_page(soup, current_url)
            current_url = next_url
            if current_url:
                time.sleep(10)

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete. Created {created} languages, updated {updated}."
            )
        )

    def _normalize_header(self, value: str) -> str:
        return " ".join(value.lower().split())

    def _get_column_value(self, headers, data, names):
        for name in names:
            name_normalized = self._normalize_header(name)
            for idx, header in enumerate(headers):
                if header == name_normalized:
                    return data[idx] if idx < len(data) else ""
        return ""

    def _parse_iso2_iso5(self, combined: str):
        """
        Parse the combined 639-2/639-5 field.
        The table sometimes contains two values; we map the first three-letter
        code to iso_set_639_2_code and the second (if present) to iso_set_639_5_code.
        """
        if not combined:
            return None, None

        tokens = re.findall(r"[A-Za-z]{3,}", combined)
        iso2 = tokens[0][:3] if tokens else None
        iso5 = tokens[1][:3] if len(tokens) > 1 else None
        return iso2, iso5

    def _fetch_with_retry(self, session, url, timeout=30):
        """
        Perform a GET with a short retry on 403 (likely bot protection)
        to allow a pause and retry once.
        """
        response = session.get(url, timeout=timeout)
        if response.status_code == 403:
            time.sleep(5)
            response = session.get(url, timeout=timeout)
        return response

    def _find_next_page(self, soup, current_url):
        # Try rel="next"
        rel_next = soup.find("a", rel="next")
        if rel_next and rel_next.get("href"):
            return urljoin(current_url, rel_next["href"])

        # Drupal-style pager items (class may be pager-next or pager__item--next)
        pager_next = soup.find("li", class_=re.compile(r"pager(-|__item--)next"))
        if pager_next:
            link = pager_next.find("a")
            if link and link.get("href"):
                return urljoin(current_url, link["href"])

        # Fallback: any <ul class="pager"> with a pager-next item
        pager_ul = soup.find("ul", class_=re.compile(r"pager"))
        if pager_ul:
            pager_link = pager_ul.find("li", class_=re.compile(r"pager-next"))
            if pager_link:
                link = pager_link.find("a")
                if link and link.get("href"):
                    return urljoin(current_url, link["href"])

        # Try text-based match
        for link in soup.find_all("a"):
            text = (link.get_text() or "").strip().lower()
            if text in {"next", "next ›", "›", "››", "next page"} and link.get("href"):
                return urljoin(current_url, link["href"])

        return None
