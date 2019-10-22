from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "threads"
urlpatterns = [
    path(
        "by-entity/<str:content_provider_id>/<str:entity_id>/",
        views.index,
        name="index",
    ),
    path(
        "add-comment/<str:thread_id>/comments/",
        views.create_comment,
        name="create_comment",
    ),
]
