from django.urls import path

from .views import (
    ChatAPIView,
    PhoneCompareAPIView,
    PhoneDetailAPIView,
    PhoneListAPIView,
)


urlpatterns = [
    path(
        "",
        PhoneListAPIView.as_view(),
        name="phone-list",
    ),
    path(
        "compare/",
        PhoneCompareAPIView.as_view(),
        name="phone-compare",
    ),
    path(
        "chat/",
        ChatAPIView.as_view(),
        name="phone-chat",
    ),
    path(
        "<int:pk>/",
        PhoneDetailAPIView.as_view(),
        name="phone-detail",
    ),
]