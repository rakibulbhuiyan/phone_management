import requests

from bs4 import BeautifulSoup


class GSMArenaScraper:

    def __init__(self, url):
        self.url = url

    def fetch_page(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 "
                "Safari/537.36"
            )
        }

        response = requests.get(
            self.url,
            headers=headers,
            timeout=20,
        )

        response.raise_for_status()

        return response.text

    def get_section(self, soup, section_name):
        for table in soup.select("table"):
            heading = table.select_one("tr th")

            if not heading:
                continue

            title = heading.get_text(
                " ",
                strip=True,
            )

            if title.lower() == section_name.lower():
                return table

        return None

    def get_section_value(
        self,
        section,
        label,
    ):
        if not section:
            return ""

        for row in section.select("tr"):
            label_element = row.select_one("td.ttl")
            value_element = row.select_one("td.nfo")

            if not label_element or not value_element:
                continue

            current_label = label_element.get_text(
                " ",
                strip=True,
            )

            if current_label.lower() == label.lower():
                return value_element.get_text(
                    " ",
                    strip=True,
                )

        return ""

    def get_camera_modules(self, section):
        if not section:
            return ""

        camera_element = section.select_one(
            '[data-spec="cam1modules"]'
        )

        if not camera_element:
            return ""

        return camera_element.get_text(
            " ",
            strip=True,
        )

    def parse_memory(self, memory_value):
        if not memory_value:
            return {
                "ram": "",
                "storage": "",
            }

        storage_list = []
        ram_list = []

        for variant in memory_value.split(","):
            variant = variant.strip()

            parts = variant.split()

            if len(parts) < 2:
                continue

            storage = parts[0]
            ram = " ".join(parts[1:])

            if storage not in storage_list:
                storage_list.append(storage)

            if ram not in ram_list:
                ram_list.append(ram)

        return {
            "ram": " / ".join(ram_list),
            "storage": " / ".join(storage_list),
        }

    def parse(self, html):
        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        # -------------------------
        # Phone name
        # -------------------------

        phone_name = soup.select_one(
            "h1.specs-phone-name-title"
        )

        if phone_name:
            phone_name = phone_name.get_text(
                strip=True,
            )
        else:
            phone_name = ""

        # -------------------------
        # Find specification sections
        # -------------------------

        display = self.get_section(
            soup,
            "Display",
        )

        platform = self.get_section(
            soup,
            "Platform",
        )

        memory = self.get_section(
            soup,
            "Memory",
        )

        main_camera = self.get_section(
            soup,
            "Main Camera",
        )

        selfie_camera = self.get_section(
            soup,
            "Selfie camera",
        )

        battery = self.get_section(
            soup,
            "Battery",
        )

        # -------------------------
        # Parse memory
        # -------------------------

        memory_value = self.get_section_value(
            memory,
            "Internal",
        )

        parsed_memory = self.parse_memory(
            memory_value,
        )

        # -------------------------
        # Return scraped data
        # -------------------------

        return {
            "name": phone_name,

            "display_size": self.get_section_value(
                display,
                "Size",
            ),

            "display_type": self.get_section_value(
                display,
                "Type",
            ),

            "processor": self.get_section_value(
                platform,
                "Chipset",
            ),

            "ram": parsed_memory["ram"],

            "storage": parsed_memory["storage"],

            "main_camera": self.get_camera_modules(
                main_camera,
            ),

            "selfie_camera": self.get_section_value(
                selfie_camera,
                "Single",
            ),

            "battery": self.get_section_value(
                battery,
                "Type",
            ),

            "operating_system": self.get_section_value(
                platform,
                "OS",
            ),
        }

    def scrape(self):
        html = self.fetch_page()

        return self.parse(html)