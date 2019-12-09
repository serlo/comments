from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "threads"
urlpatterns = [
    path("<str:content_provider_id>/<str:entity_id>/", views.index, name="index",)
]
