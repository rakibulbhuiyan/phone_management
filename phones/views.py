from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Phone
from .serializers import PhoneSerializer
from .services.phone_context import PhoneContextBuilder
from .services.query_processor import PhoneQueryProcessor
from .services.llm_service import PhoneLLMService

class PhoneListAPIView(generics.ListAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

    filter_backends = [
        filters.SearchFilter,
    ]

    search_fields = [
        "name",
        "processor",
        "display_type",
        "ram",
        "storage",
        "operating_system",
    ]


class PhoneDetailAPIView(generics.RetrieveAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class PhoneCompareAPIView(APIView):

    def post(self, request):
        phone1_id = request.data.get("phone1")
        phone2_id = request.data.get("phone2")

        if not phone1_id or not phone2_id:
            return Response(
                {
                    "error": (
                        "phone1 and phone2 are required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            phone1 = Phone.objects.get(
                id=phone1_id
            )
        except Phone.DoesNotExist:
            return Response(
                {
                    "error": (
                        f"Phone with id "
                        f"{phone1_id} not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            phone2 = Phone.objects.get(
                id=phone2_id
            )
        except Phone.DoesNotExist:
            return Response(
                {
                    "error": (
                        f"Phone with id "
                        f"{phone2_id} not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "phone1": PhoneSerializer(
                    phone1
                ).data,
                "phone2": PhoneSerializer(
                    phone2
                ).data,
            },
            status=status.HTTP_200_OK,
        )


class ChatAPIView(APIView):

    def post(self, request):
        message = request.data.get("message")

        if not message:
            return Response(
                {
                    "error": "message is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        processor = PhoneQueryProcessor()

        phones = processor.extract_phones(
            message
        )

        if not phones.exists():
            return Response(
                {
                    "answer": (
                        "I could not find any "
                        "matching Samsung phone "
                        "in the database."
                    ),
                    "phones_found": [],
                },
                status=status.HTTP_200_OK,
            )

        context_builder = PhoneContextBuilder()

        context = context_builder.build(
            phones
        )

        try:
            llm_service = PhoneLLMService()

            answer = llm_service.generate_answer(
                question=message,
                context=context,
            )

        except Exception as error:
            return Response(
                {
                    "error": "Failed to generate answer.",
                    "details": str(error),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "question": message,
                "phones_found": list(
                    phones.values_list(
                        "name",
                        flat=True
                    )
                ),
                "answer": answer,
            },
            status=status.HTTP_200_OK,
        )