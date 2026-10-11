
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import FileResponse
from django.urls import path

from assistant import views


def service_worker(request):
    file_path = Path(settings.BASE_DIR) / "static" / "service-worker.js"
    return FileResponse(
        file_path.open("rb"),
        content_type="application/javascript"
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("ask/", views.ask_gemini, name="ask_gemini"),
    path("service-worker.js", service_worker, name="service_worker"),
]
