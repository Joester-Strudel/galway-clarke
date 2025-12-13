import csv
from django.core.management.base import BaseCommand
from ...models.state import State, County, City, ZipCode


class Command(BaseCommand):
    help = "Import geography data from a hardcoded CSV file and create or update relevant Django objects."

    def handle(self, *args, **options):
        # Hard-code the CSV file path
        csv_file_path = "gc_geography/seeds/uszips.csv"

        with open(csv_file_path, "r") as file:
            reader = csv.DictReader(file)

            # Limit to the first 1000 records for testing
            for idx, row in enumerate(reader):
                # Get or create State
                state, _ = State.objects.get_or_create(
                    abbreviation=row["state_id"], defaults={"name": row["state_name"]}
                )

                # Get or create County, ensuring the County is correctly linked to the State
                county, _ = County.objects.get_or_create(
                    fips_code=row["county_fips"],
                    defaults={"name": row["county_name"], "state": state},
                )

                # Get or create City, ensuring the City is correctly linked to both State and County
                city, _ = City.objects.get_or_create(
                    name=row["city"],
                    state=state,  # Include state in the lookup
                    defaults={"county": county},
                )

                # Get or create ZipCode, ensuring the ZipCode is correctly linked
                zipcode, _ = ZipCode.objects.get_or_create(
                    zip_code_five_digit=row["zip"],
                    defaults={
                        "population": int(row["population"]) if row["population"] else None,
                        "density": float(row["density"]) if row["density"] else None,
                    },
                )

                # Link ZipCode to State, County, and City (many-to-many relationships)
                if state not in zipcode.states.all():
                    zipcode.states.add(state)
                if county not in zipcode.counties.all():
                    zipcode.counties.add(county)
                if city not in zipcode.cities.all():
                    zipcode.cities.add(city)

        self.stdout.write(self.style.SUCCESS("Geography data imported successfully."))