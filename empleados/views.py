from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import (
    Cargo,
    Departamento,
    TipoContrato,
    Empleado,
    Rol,
    Sobretiempo,
    TipoSobretiempo,
)
from .forms import (
    CargoForm,
    DepartamentoForm,
    TipoContratoForm,
    EmpleadoForm,
    RolForm,
    SobretiempoForm,
)
from django.http import HttpResponseForbidden


# Vista inicial del sistema. Redirige al dashboard si el usuario está autenticado, o muestra la página de inicio si no lo está.
def home(request):
    if request.user.is_authenticated:
        return redirect("empleados:dashboard")
    return render(request, "home.html")


# Vista para registrar nuevos usuarios. Verifica contraseñas y maneja errores de usuario duplicado.
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("empleados:home")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {
                        "form": UserCreationForm,
                        "error": "El usuario ya existe",
                    },
                )
        else:
            return render(
                request,
                "signup.html",
                {
                    "form": UserCreationForm,
                    "error": "Las contraseñas no coinciden",
                },
            )


# Vista para iniciar sesión. Autentica al usuario y lo redirige al dashboard si las credenciales son correctas.
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm,
                    "error": "Usuario o contraseña incorrectos",
                },
            )
        else:
            login(request, user)
            return redirect("empleados:dashboard")
    return render(request, "login.html", {"form": AuthenticationForm})


# Vista para cerrar sesión. Redirige al usuario a la página de inicio.
@login_required
def logout_view(request):
    logout(request)
    return redirect("empleados:home")


# Vistas para Cargo
# Vista para listar cargos. Permite búsqueda y paginación.
@login_required
def cargo_list(request):
    query = request.GET.get("q", None)
    if query:
        cargos = Cargo.objects.filter(descripcion__icontains=query)
    else:
        cargos = Cargo.objects.all()

    # Paginación
    paginator = Paginator(cargos, 5)  # 5 items por página
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {"page_obj": page_obj, "title": "Listado de Cargos"}
    return render(request, "cargo/list.html", context)


# Vista para crear un nuevo cargo. Asocia el cargo al usuario actual.
@login_required
def cargo_create(request):
    context = {"title": "Crear Cargo"}
    if request.method == "POST":
        form = CargoForm(request.POST)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.user = request.user
            cargo.save()
            messages.success(request, "Cargo creado exitosamente")
            return redirect("empleados:cargo_list")
    else:
        form = CargoForm()
    context["form"] = form
    return render(request, "cargo/form.html", context)


# Vista para actualizar un cargo existente. Verifica que el usuario sea el propietario del cargo.
@login_required
def cargo_update(request, id):
    context = {"title": "Actualizar Cargo"}
    cargo = get_object_or_404(Cargo, pk=id)
    if cargo.user != request.user:
        return redirect("empleados:dashboard")
    if request.method == "POST":
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, "Cargo actualizado exitosamente")
            return redirect("empleados:cargo_list")
    else:
        form = CargoForm(instance=cargo)
    context["form"] = form
    return render(request, "cargo/form.html", context)


# Vista para eliminar un cargo existente. Redirige a la lista de cargos tras la eliminación.
@login_required
def cargo_delete(request, id):
    cargo = get_object_or_404(Cargo, pk=id)
    cargo.delete()
    messages.success(request, "Cargo eliminado exitosamente")
    return redirect("empleados:cargo_list")


# Vistas para Departamento
# Vista para listar departamentos. Permite búsqueda y paginación.
@login_required
def departamento_list(request):
    query = request.GET.get("q", None)
    if query:
        departamentos = Departamento.objects.filter(
            descripcion__icontains=query, user=request.user
        )
    else:
        departamentos = Departamento.objects.filter(user=request.user)

    # Paginación
    paginator = Paginator(departamentos, 5)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {"page_obj": page_obj, "title": "Listado de Departamentos"}
    return render(request, "departamento/list.html", context)


# Vista para crear un nuevo departamento. Asocia el departamento al usuario actual.
@login_required
def departamento_create(request):
    context = {"title": "Crear Departamento"}
    if request.method == "POST":
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            departamento = form.save(commit=False)
            departamento.user = request.user
            departamento.save()
            messages.success(request, "Departamento creado exitosamente")
            return redirect("empleados:departamento_list")
    else:
        form = DepartamentoForm()
    context["form"] = form
    return render(request, "departamento/form.html", context)


# Vista para actualizar un departamento existente. Verifica que el usuario sea el propietario del departamento.
@login_required
def departamento_update(request, id):
    context = {"title": "Actualizar Departamento"}
    departamento = get_object_or_404(Departamento, pk=id)
    if departamento.user != request.user:
        return redirect("empleados:dashboard")
    if request.method == "POST":
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento actualizado exitosamente")
            return redirect("empleados:departamento_list")
    else:
        form = DepartamentoForm(instance=departamento)
    context["form"] = form
    return render(request, "departamento/form.html", context)


# Vista para eliminar un departamento existente. Redirige a la lista de departamentos tras la eliminación.
@login_required
def departamento_delete(request, id):
    departamento = get_object_or_404(Departamento, pk=id)
    departamento.delete()
    messages.success(request, "Departamento eliminado exitosamente")
    return redirect("empleados:departamento_list")


# Vistas para TipoContrato
# Vista para listar tipos de contrato. Permite búsqueda y paginación.
@login_required
def tipo_contrato_list(request):
    query = request.GET.get("q", None)
    if query:
        tipos = TipoContrato.objects.filter(
            descripcion__icontains=query, user=request.user
        )
    else:
        tipos = TipoContrato.objects.filter(user=request.user)

    # Paginación
    paginator = Paginator(tipos, 5)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {"page_obj": page_obj, "title": "Listado de Tipos de Contrato"}
    return render(request, "tipo_contrato/list.html", context)


# Vista para crear un nuevo tipo de contrato. Asocia el tipo de contrato al usuario actual.
@login_required
def tipo_contrato_create(request):
    context = {"title": "Crear Tipo de Contrato"}
    if request.method == "POST":
        form = TipoContratoForm(request.POST)
        if form.is_valid():
            tipo_contrato = form.save(commit=False)
            tipo_contrato.user = request.user
            tipo_contrato.save()
            messages.success(request, "Tipo de contrato creado exitosamente")
            return redirect("empleados:tipo_contrato_list")
    else:
        form = TipoContratoForm()
    context["form"] = form
    return render(request, "tipo_contrato/form.html", context)


# Vista para actualizar un tipo de contrato existente.
@login_required
def tipo_contrato_update(request, id):
    context = {"title": "Actualizar Tipo de Contrato"}
    tipo = get_object_or_404(TipoContrato, pk=id)
    if request.method == "POST":
        form = TipoContratoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de contrato actualizado exitosamente")
            return redirect("empleados:tipo_contrato_list")
    else:
        form = TipoContratoForm(instance=tipo)
    context["form"] = form
    return render(request, "tipo_contrato/form.html", context)


# Vista para eliminar un tipo de contrato existente. Redirige a la lista de tipos de contrato tras la eliminación.
@login_required
def tipo_contrato_delete(request, id):
    tipo = get_object_or_404(TipoContrato, pk=id)
    tipo.delete()
    messages.success(request, "Tipo de contrato eliminado exitosamente")
    return redirect("empleados:tipo_contrato_list")


# Vistas para Empleado
# Vista para listar empleados. Permite búsqueda y paginación.
@login_required
def empleado_list(request):
    query = request.GET.get("q", None)
    if query:
        empleados = Empleado.objects.filter(nombre__icontains=query)
    else:
        empleados = Empleado.objects.all()

    # Paginación
    paginator = Paginator(empleados, 5)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {"page_obj": page_obj, "title": "Listado de Empleados"}
    return render(request, "empleado/list.html", context)


# Vista para crear un nuevo empleado.
@login_required
def empleado_create(request):
    context = {"title": "Crear Empleado"}
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado creado exitosamente")
            return redirect("empleados:empleado_list")
    else:
        form = EmpleadoForm()
    context["form"] = form
    return render(request, "empleado/form.html", context)


# Vista para actualizar un empleado existente.
@login_required
def empleado_update(request, id):
    context = {"title": "Actualizar Empleado"}
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado actualizado exitosamente")
            return redirect("empleados:empleado_list")
    else:
        form = EmpleadoForm(instance=empleado)
    context["form"] = form
    return render(request, "empleado/form.html", context)


# Vista para eliminar un empleado existente. Redirige a la lista de empleados tras la eliminación.
@login_required
def empleado_delete(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    empleado.delete()
    messages.success(request, "Empleado eliminado exitosamente")
    return redirect("empleados:empleado_list")


# Vistas para Rol
# Vista para listar roles de pago. Permite búsqueda y paginación.
@login_required
def rol_list(request):
    query = request.GET.get("q", None)
    if query:
        roles = Rol.objects.filter(empleado__nombre__icontains=query)
    else:
        roles = Rol.objects.all()

    # Paginación
    paginator = Paginator(roles, 5)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {"page_obj": page_obj, "title": "Listado de Roles de Pago"}
    return render(request, "rol/list.html", context)


# Vista para crear un nuevo rol de pago.
@login_required
def rol_create(request):
    context = {"title": "Crear Rol de Pago"}
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol de pago creado exitosamente")
            return redirect("empleados:rol_list")
    else:
        form = RolForm()
    context["form"] = form
    return render(request, "rol/form.html", context)


# Vista para actualizar un rol de pago existente.
@login_required
def rol_update(request, id):
    context = {"title": "Actualizar Rol de Pago"}
    rol = get_object_or_404(Rol, pk=id)
    if request.method == "POST":
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol de pago actualizado exitosamente")
            return redirect("empleados:rol_list")
    else:
        form = RolForm(instance=rol)
    context["form"] = form
    return render(request, "rol/form.html", context)


# Vista para eliminar un rol de pago existente. Redirige a la lista de roles tras la eliminación.
@login_required
def rol_delete(request, id):
    rol = get_object_or_404(Rol, pk=id)
    rol.delete()
    messages.success(request, "Rol de pago eliminado exitosamente")
    return redirect("empleados:rol_list")


# Vista para mostrar el dashboard principal del sistema.
@login_required
def dashboard(request):
    return render(request, "dashboard.html")


# Vistas CRUD para la gestión de Sobretiempo


# Vista para listar todos los registros de sobretiempo.
@login_required
def sobretiempo_list(request):
    sobretiempos = Sobretiempo.objects.all()
    empleados = Empleado.objects.all()
    tipos = TipoSobretiempo.objects.all()
    # ...filtros si quieres...
    context = {
        "sobretiempos": sobretiempos,
        "empleados": empleados,
        "tipos": tipos,
    }
    return render(request, "sobretiempo/list.html", context)


# Vista para crear un nuevo registro
# Muestra un formulario y si es válido guarda el registro y redirige al listado.
@login_required
def sobretiempo_create(request):
    if request.method == "POST":
        form = SobretiempoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sobretiempo creado exitosamente")
            return redirect("empleados:sobretiempo_list")
    else:
        form = SobretiempoForm()
    return render(
        request, "sobretiempo/form.html", {"form": form, "title": "Crear Sobretiempo"}
    )


# Vista para actualizar un registro
@login_required
def sobretiempo_update(request, id):
    sobretiempo = get_object_or_404(Sobretiempo, pk=id)
    if request.method == "POST":
        form = SobretiempoForm(request.POST, instance=sobretiempo)
        if form.is_valid():
            form.save()
            messages.success(request, "Sobretiempo actualizado exitosamente")
            return redirect("empleados:sobretiempo_list")
    else:
        form = SobretiempoForm(instance=sobretiempo)
    return render(
        request,
        "sobretiempo/form.html",
        {"form": form, "title": "Actualizar Sobretiempo"},
    )


# Vista para eliminar
@login_required
def sobretiempo_delete(request, id):
    sobretiempo = get_object_or_404(Sobretiempo, pk=id)
    if request.method == "POST":
        sobretiempo.delete()
        messages.success(request, "Sobretiempo eliminado exitosamente")
        return redirect("empleados:sobretiempo_list")
    return render(request, "sobretiempo/delete.html", {"sobretiempo": sobretiempo})
