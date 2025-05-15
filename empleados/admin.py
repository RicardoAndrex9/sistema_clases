# App empleados/admin.py
from django.contrib import admin
from .models import (
    Cargo,
    Departamento,
    TipoContrato,
    Empleado,
    Rol,
    TipoSobretiempo,
    Sobretiempo,
)

admin.site.register(Cargo)
admin.site.register(Departamento)
admin.site.register(TipoContrato)
admin.site.register(Empleado)
admin.site.register(Rol)

# Admin
admin.site.register(TipoSobretiempo)
admin.site.register(Sobretiempo)
