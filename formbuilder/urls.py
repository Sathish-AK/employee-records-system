from django.urls import path
from . import views

urlpatterns = [
    path("", views.form_list, name="form_list"),
    path("new/", views.form_new, name="form_new"),
    path("<int:pk>/edit/", views.form_edit, name="form_edit"),
    path("<int:pk>/delete/", views.form_delete, name="form_delete"),
]
