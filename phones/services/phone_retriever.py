from django.db.models import Q

from phones.models import Phone


class PhoneRetriever:

    def search(self, query):
        if not query:
            return Phone.objects.none()

        query = query.strip()

        # First try exact phone-name matching.
        exact_matches = Phone.objects.filter(
            name__icontains=query
        )

        if exact_matches.exists():
            return exact_matches

        # Search individual words across phone fields.
        words = query.split()

        conditions = Q()

        for word in words:
            if len(word) < 2:
                continue

            conditions |= (
                Q(name__icontains=word)
                | Q(processor__icontains=word)
                | Q(display_type__icontains=word)
                | Q(ram__icontains=word)
                | Q(storage__icontains=word)
                | Q(battery__icontains=word)
                | Q(main_camera__icontains=word)
                | Q(selfie_camera__icontains=word)
                | Q(operating_system__icontains=word)
            )

        return Phone.objects.filter(
            conditions
        ).distinct()