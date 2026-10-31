from django.urls import path
from . import views


app_name = "purchases"


urlpatterns = [

    path(
        "",
        views.purchase_list,
        name="list"
    ),

    path(
        "add/",
        views.purchase_create,
        name="create"
    ),

    path(
        "<int:pk>/edit/",
        views.purchase_edit,
        name="edit"
    ),

    path(
        "<int:pk>/delete/",
        views.purchase_delete,
        name="delete"
    ),

]