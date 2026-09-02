from django.core.management.base import BaseCommand

from phones.models import Phone
from phones.scraper.gsmarena import GSMArenaScraper


PHONE_URLS = [
    "https://www.gsmarena.com/samsung_galaxy_s21_5g-10631.php",
    "https://www.gsmarena.com/samsung_galaxy_s21_ultra_5g-10596.php",
    "https://www.gsmarena.com/samsung_galaxy_s22_5g-11253.php",
    "https://www.gsmarena.com/samsung_galaxy_s22_ultra_5g-11251.php",
    "https://www.gsmarena.com/samsung_galaxy_s23-12082.php",
    "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12024.php",
    "https://www.gsmarena.com/samsung_galaxy_s24-12773.php",
    "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php",
]


class Command(BaseCommand):
    help = "Scrape Samsung phone data and save to database"

    def handle(self, *args, **options):

        for url in PHONE_URLS:

            self.stdout.write(
                f"\nScraping: {url}"
            )

            try:
                scraper = GSMArenaScraper(url)

                data = scraper.scrape()

                if not data["name"]:
                    self.stdout.write(
                        self.style.WARNING(
                            "Phone name not found. Skipping."
                        )
                    )
                    continue

                phone, created = Phone.objects.update_or_create(
                    name=data["name"],
                    defaults={
                        "display_size": data["display_size"],
                        "display_type": data["display_type"],
                        "processor": data["processor"],
                        "ram": data["ram"],
                        "storage": data["storage"],
                        "battery": data["battery"],
                        "main_camera": data["main_camera"],
                        "selfie_camera": data["selfie_camera"],
                        "operating_system": data["operating_system"],
                        "source_url": url,
                    },
                )

                if created:
                    status = "Created"
                else:
                    status = "Updated"

                self.stdout.write(
                    self.style.SUCCESS(
                        f"{status}: {phone.name}"
                    )
                )

            except Exception as error:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed: {url}"
                    )
                )

                self.stdout.write(
                    self.style.ERROR(
                        f"Error: {error}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "\nScraping completed."
            )
        )