from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("redirect", views.redirect_index),
    path("users/<int:user_id>", views.get_user),
    path("list", views.list_view, name="list_view"),
]