from django.forms import ModelForm, TextInput, NumberInput, Select, DateInput
from django import forms
from .models import Cargo, Departamento, TipoContrato, Empleado, Rol


class CargoForm(ModelForm):
    class Meta:
        model = Cargo
        exclude = ["user"]
        widgets = {
            "descripcion": TextInput(attrs={"class": "form-control"}),
        }


class DepartamentoForm(ModelForm):
    class Meta:
        model = Departamento
        exclude = ["user"]
        widgets = {
            "descripcion": TextInput(attrs={"class": "form-control"}),
        }


class TipoContratoForm(ModelForm):
    class Meta:
        model = TipoContrato
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "descripcion": TextInput(attrs={"class": "form-control"}),
        }


class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "nombre": TextInput(attrs={"class": "form-control"}),
            "cedula": TextInput(attrs={"class": "form-control"}),
            "direccion": TextInput(attrs={"class": "form-control"}),
            "sexo": Select(attrs={"class": "form-control"}),
            "sueldo": NumberInput(attrs={"class": "form-control"}),
            "cargo": Select(attrs={"class": "form-control"}),
            "departamento": Select(attrs={"class": "form-control"}),
            "tipo_contrato": Select(attrs={"class": "form-control"}),
        }


class RolForm(ModelForm):
    class Meta:
        model = Rol
        fields = ["empleado", "aniomes", "sueldo", "horas_extra", "bono"]
        exclude = ["user"]
        widgets = {
            "empleado": Select(attrs={"class": "form-control"}),
            "aniomes": DateInput(attrs={"class": "form-control", "type": "date"}),
            "sueldo": NumberInput(attrs={"class": "form-control"}),
            "horas_extra": NumberInput(attrs={"class": "form-control"}),
            "bono": NumberInput(attrs={"class": "form-control"}),
        }
