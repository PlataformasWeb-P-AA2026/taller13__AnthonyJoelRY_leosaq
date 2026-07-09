from django.urls import path, include

# Se importan las vistas de la aplicación
from inmuebles import views

# Django REST Framework
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"edificios", views.EdificioViewSet)
router.register(r"departamentos", views.DepartamentoViewSet)


urlpatterns = [
    # Página principal / menú
    path("", views.index, name="index"),

    # Edificios
    path("edificios/", views.listar_edificios, name="listar_edificios"),
    path("edificio/<int:id>", views.obtener_edificio, name="obtener_edificio"),
    path("crear/edificio", views.crear_edificio, name="crear_edificio"),
    path("editar/edificio/<int:id>", views.editar_edificio, name="editar_edificio"),
    path(
        "eliminar/edificio/<int:id>",
        views.eliminar_edificio,
        name="eliminar_edificio",
    ),

    # Departamentos
    path(
        "departamentos/",
        views.listar_departamentos,
        name="listar_departamentos",
    ),
    path(
        "departamento/<int:id>",
        views.obtener_departamento,
        name="obtener_departamento",
    ),
    path(
        "crear/departamento",
        views.crear_departamento,
        name="crear_departamento",
    ),
    path(
        "editar/departamento/<int:id>",
        views.editar_departamento,
        name="editar_departamento",
    ),
    path(
        "eliminar/departamento/<int:id>",
        views.eliminar_departamento,
        name="eliminar_departamento",
    ),

    # Login y logout
    path("saliendo/logout/", views.logout_view, name="logout_view"),
    path("entrando/login/", views.ingreso, name="login"),

    # API REST
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]