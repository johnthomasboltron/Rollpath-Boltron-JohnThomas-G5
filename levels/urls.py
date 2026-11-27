from django.urls import path
from . import views

urlpatterns = [
    path("", views.level_list, name="level_list"),
    path("create/", views.level_create, name="level_create"),
    path("<int:pk>/", views.level_detail, name="level_detail"),
    path("<int:pk>/edit/", views.level_update, name="level_update"),
    path("<int:pk>/delete/", views.level_delete, name="level_delete"),
    path("<int:pk>/publish/", views.level_publish, name="level_publish"),
    path("<int:pk>/editor/", views.level_editor, name="level_editor"),
    path("<int:pk>/elements/<int:element_pk>/delete/",views.level_element_delete,name="level_element_delete"),
    path("<int:pk>/elements/<int:element_pk>/move/",views.level_element_move,name="level_element_move"),
    path(
    "<int:pk>/elements/<int:element_pk>/resize/",
    views.level_element_resize,
    name="level_element_resize"
),
]
