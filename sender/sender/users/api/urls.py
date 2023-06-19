from django.urls import include, path

from sender.users.api import views

app_name = "users"

urlpatterns = [
    path(
        "user/",
        include(
            [
                path("sender/", views.SenderView.as_view(), name="sender-view"),
            ]
        ),
    ),
]
