
from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.sale_list, name="list"),
    path("create/", views.sale_create, name="create"),
    path("<int:pk>/edit/", views.sale_edit, name="edit"),
    path("<int:pk>/delete/", views.sale_delete, name="delete"),
    path("<int:pk>/details/", views.sale_detail, name="detail"),
]