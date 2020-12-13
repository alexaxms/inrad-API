from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url(
        r"^v1/",
        include("api.v1.urls", namespace="v1"),
        name="api",
    )
]