from django.urls import path

from app.views import CheckAPIKeyAuthenticationApi, GetUserInformationApi

urlpatterns = [
    path("check/", CheckAPIKeyAuthenticationApi.as_view(), name="check-api-key"),
    path(
        "user-information/",
        GetUserInformationApi.as_view(),
        name="get-user-information",
    ),
]
