import re

from phones.models import Phone


class PhoneQueryProcessor:

    def extract_phones(self, query):
        if not query:
            return Phone.objects.none()

        query = query.strip().lower()

        all_phones = Phone.objects.all()

        matched_phone_ids = []

        for phone in all_phones:
            phone_name = phone.name.lower()

            if phone_name in query:
                matched_phone_ids.append(phone.id)
                continue

            model_match = re.search(
                r"s\d+",
                phone_name,
            )

            if model_match:
                model = model_match.group(0)

                if re.search(
                    rf"\b{model}\b",
                    query,
                ):
                    matched_phone_ids.append(
                        phone.id
                    )

        return Phone.objects.filter(
            id__in=matched_phone_ids
        )