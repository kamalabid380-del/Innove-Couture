from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("collections/<slug:slug>/", views.collection_detail, name="collection"),
    path("looks/<slug:slug>/", views.look_detail, name="look"),
    path("contact/", views.contact, name="contact"),
]
