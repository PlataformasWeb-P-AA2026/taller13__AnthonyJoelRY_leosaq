"""
    Manejo de urls para la aplicación
    administrativo (Edificios y Departamentos)
"""
from django.urls import path, include
# se importa las vistas de la aplicación
from administrativo import views
from rest_framework import routers

router = routers.DefaultRouter()
# --- Endpoints de la API REST ---
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'edificios', views.EdificioViewSet)          
router.register(r'departamentos', views.DepartamentoViewSet)  


urlpatterns = [
        # --- Vista de inicio ---
        path('', views.index, name='index'),
        
        # Rutas para Edificios (Jinja2 Templates locales)
        path('los/edificios/', views.listar_edificios, name='listar_edificios'),
        path('crear/edificio/', views.crear_edificio, name='crear_edificio'),
        path('editar/edificio/<int:id>/', views.editar_edificio, name='editar_edificio'),
        path('eliminar/edificio/<int:id>/', views.eliminar_edificio, name='eliminar_edificio'),
        
        # Rutas para Departamentos (Jinja2 Templates locales)
        path('los/departamentos/', views.listar_departamentos, name='listar_departamentos'),
        path('crear/departamento/', views.crear_departamento, name='crear_departamento'),
        path('editar/departamento/<int:id>/', views.editar_departamento, name='editar_departamento'),
        path('eliminar/departamento/<int:id>/', views.eliminar_departamento, name='eliminar_departamento'),
        
        # Ruta específica para crear un departamento directamente desde un edificio
        path('crear/departamento/edificio/<int:id>/', 
            views.crear_departamento_edificio, 
            name='crear_departamento_edificio'),

        # --- Autenticación y API REST Endpoints ---
        path('saliendo/logout/', views.logout_view, name="logout_view"),
        path('entrando/login/', views.ingreso, name="login"),
        
        # AJUSTE: Mapeo limpio de la API con barra inclinada
        path('api/', include((router.urls, 'api'))),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]