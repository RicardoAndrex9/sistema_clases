# empleados/urls.py
from django.urls import path
from . import views

app_name = "empleados"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    # URLs para Cargo
    path("cargos/", views.cargo_list, name="cargo_list"),
    path("cargos/crear/", views.cargo_create, name="cargo_create"),
    path("cargos/<int:id>/editar/", views.cargo_update, name="cargo_update"),
    path("cargos/<int:id>/eliminar/", views.cargo_delete, name="cargo_delete"),
    # URLs para Departamento
    path("departamentos/", views.departamento_list, name="departamento_list"),
    path("departamentos/crear/", views.departamento_create, name="departamento_create"),
    path(
        "departamentos/<int:id>/editar/",
        views.departamento_update,
        name="departamento_update",
    ),
    path(
        "departamentos/<int:id>/eliminar/",
        views.departamento_delete,
        name="departamento_delete",
    ),
    # URLs para TipoContrato
    path("tipos-contrato/", views.tipo_contrato_list, name="tipo_contrato_list"),
    path(
        "tipos-contrato/crear/", views.tipo_contrato_create, name="tipo_contrato_create"
    ),
    path(
        "tipos-contrato/<int:id>/editar/",
        views.tipo_contrato_update,
        name="tipo_contrato_update",
    ),
    path(
        "tipos-contrato/<int:id>/eliminar/",
        views.tipo_contrato_delete,
        name="tipo_contrato_delete",
    ),
    # URLs para Empleado
    path("empleados/", views.empleado_list, name="empleado_list"),
    path("empleados/crear/", views.empleado_create, name="empleado_create"),
    path("empleados/<int:id>/editar/", views.empleado_update, name="empleado_update"),
    path("empleados/<int:id>/eliminar/", views.empleado_delete, name="empleado_delete"),
    # URLs para Rol
    path("roles/", views.rol_list, name="rol_list"),
    path("roles/crear/", views.rol_create, name="rol_create"),
    path("roles/<int:id>/editar/", views.rol_update, name="rol_update"),
    path("roles/<int:id>/eliminar/", views.rol_delete, name="rol_delete"),
    
    
    # URLs creadas para el examen
    path("sobretiempo/", views.sobretiempo_list, name="sobretiempo_list"),
    path("sobretiempo/crear/", views.sobretiempo_create, name="sobretiempo_create"),
    path(
        "sobretiempo/<int:id>/editar/",
        views.sobretiempo_update,
        name="sobretiempo_update",
    ),
    path(
        "sobretiempo/<int:id>/eliminar/",
        views.sobretiempo_delete,
        name="sobretiempo_delete",
    ),
]
