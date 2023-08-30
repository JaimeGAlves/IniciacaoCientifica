from django.contrib import admin
from django.urls import path
from backend.core import views
from api_integration import views as api_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", views.home, name="home"),
    path('uploadfile/', api_views.upload_file_view, name='upload-file'),
]