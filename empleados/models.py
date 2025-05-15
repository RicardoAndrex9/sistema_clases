# empleados/models.py
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


# Modelo que representa un cargo dentro de la organización.
class Cargo(models.Model):
    descripcion = models.CharField(max_length=100)  # Descripción del cargo.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Usuario asociado al cargo.

    def __str__(self):
        return self.descripcion


# Modelo que representa un departamento dentro de la organización.
class Departamento(models.Model):
    descripcion = models.CharField(max_length=100)  # Descripción del departamento.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Usuario asociado al departamento.

    def __str__(self):
        return self.descripcion


# Modelo que representa un tipo de contrato laboral.
class TipoContrato(models.Model):
    descripcion = models.CharField(max_length=100)  # Descripción del tipo de contrato.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Usuario asociado al tipo de contrato.

    def __str__(self):
        return self.descripcion


# Modelo que representa un empleado dentro de la organización.
class Empleado(models.Model):
    SEXO_CHOICES = [("M", "Masculino"), ("F", "Femenino")]  # Opciones de género.
    nombre = models.CharField(max_length=100)  # Nombre del empleado.
    cedula = models.CharField(max_length=20, unique=True)  # Cédula única del empleado.
    direccion = models.TextField()  # Dirección del empleado.
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)  # Género del empleado.
    sueldo = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Sueldo base del empleado.
    cargo = models.ForeignKey(
        Cargo, on_delete=models.CASCADE
    )  # Cargo asociado al empleado.
    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE
    )  # Departamento asociado al empleado.
    tipo_contrato = models.ForeignKey(
        TipoContrato, on_delete=models.CASCADE
    )  # Tipo de contrato del empleado.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Usuario asociado al empleado.

    def __str__(self):
        return self.nombre


# Modelo que representa un rol de pago para un empleado.
class Rol(models.Model):
    empleado = models.ForeignKey(
        Empleado, on_delete=models.CASCADE
    )  # Empleado asociado al rol de pago.
    aniomes = models.DateField()  # Año y mes del rol de pago.
    sueldo = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Sueldo base del empleado.
    horas_extra = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Horas extra trabajadas.
    bono = models.DecimalField(max_digits=10, decimal_places=2)  # Bonos adicionales.
    iess = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )  # Aporte al IESS (calculado automáticamente).
    tot_ing = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )  # Total de ingresos (calculado automáticamente).
    tot_des = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )  # Total de descuentos (calculado automáticamente).
    neto = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )  # Neto a recibir (calculado automáticamente).
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Usuario asociado al rol de pago.

    def save(self, *args, **kwargs):
        # Cálculos automáticos para los campos del rol de pago.
        self.tot_ing = self.sueldo + self.horas_extra + self.bono
        self.iess = self.sueldo * Decimal("0.0945")  # 9.45% del sueldo.
        self.tot_des = self.iess
        self.neto = self.tot_ing - self.tot_des
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rol de {self.empleado.nombre} - {self.aniomes}"


# Modelo sobretiempo Examen
class TipoSobretiempo(models.Model):
    descripcion = models.CharField(max_length=100)
    factor = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f"{self.descripcion} - Factor: {self.factor}"


class Sobretiempo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_sobretiempo = models.ForeignKey(TipoSobretiempo, on_delete=models.CASCADE)
    fecha_sobretiempo = models.DateField()
    numero_horas = models.DecimalField(max_digits=5, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Sobretiempo de {self.empleado.nombre} - {self.fecha_sobretiempo}"
