
from django.urls import path
from . import views

urlpatterns = [

    # INICIO
    path("", views.inicio, name="inicio"),

    # CLIENTES
    path("clientes/", views.clientes, name="clientes"),

    path("clientes/guardar/", views.guardar_cliente, name="guardar_cliente"),

    path("clientes/eliminar/<int:id>/", views.eliminar_cliente, name="eliminar_cliente"  ),

    # CITAS
    path("citas/", views.citas, name="citas"),

    path("citas/guardar/",views.guardar_cita, name="guardar_cita" ),

    path("citas/eliminar/<int:id>/",views.eliminar_cita,name="eliminar_cita" ),

]

