from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required

# Django REST Framework
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

# Serializers
from inmuebles.serializers import (
    UserSerializer,
    GroupSerializer,
    EdificioSerializer,
    DepartamentoSerializer,
)

# Modelos
from inmuebles.models import Edificio, Departamento

# Formularios
from inmuebles.forms import EdificioForm, DepartamentoForm


# Página principal
def index(request):
    """
    Presenta el menú principal del sistema.
    """
    edificios = Edificio.objects.all()
    departamentos = Departamento.objects.all()

    informacion_template = {
        "edificios": edificios,
        "departamentos": departamentos,
        "numero_edificios": len(edificios),
        "numero_departamentos": len(departamentos),
    }

    return render(request, "index.html", informacion_template)


# Login
def ingreso(request):
    """
    Permite el ingreso de usuarios al sistema.
    """
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        print(form.errors)

        if form.is_valid():
            username = form.data.get("username")
            raw_password = form.data.get("password")

            user = authenticate(username=username, password=raw_password)

            if user is not None:
                login(request, user)
                return redirect(index)
    else:
        form = AuthenticationForm()

    informacion_template = {
        "form": form
    }

    return render(request, "registration/login.html", informacion_template)


# Logout
def logout_view(request):
    """
    Permite cerrar la sesión del usuario.
    """
    logout(request)
    messages.info(request, "Has salido del sistema")
    return redirect(index)


# Listar edificios
def listar_edificios(request):
    """
    Lista todos los edificios registrados en la base de datos.
    """
    edificios = Edificio.objects.all()

    informacion_template = {
        "edificios": edificios,
        "numero_edificios": len(edificios),
    }

    return render(request, "listarEdificios.html", informacion_template)


# Listar departamentos
def listar_departamentos(request):
    """
    Lista todos los departamentos registrados en la base de datos.
    """
    departamentos = Departamento.objects.all()

    informacion_template = {
        "departamentos": departamentos,
        "numero_departamentos": len(departamentos),
    }

    return render(request, "listarDepartamentos.html", informacion_template)


# Obtener un edificio específico
def obtener_edificio(request, id):
    """
    Muestra la información de un edificio específico.
    """
    edificio = Edificio.objects.get(pk=id)

    informacion_template = {
        "edificio": edificio
    }

    return render(request, "obtenerEdificio.html", informacion_template)


# Obtener un departamento específico
def obtener_departamento(request, id):
    """
    Muestra la información de un departamento específico.
    """
    departamento = Departamento.objects.get(pk=id)

    informacion_template = {
        "departamento": departamento
    }

    return render(request, "obtenerDepartamento.html", informacion_template)


# Crear edificio
@login_required(login_url="/entrando/login/")
@permission_required("inmuebles.add_edificio", login_url="/entrando/login/")
def crear_edificio(request):
    """
    Permite crear un edificio desde Django.
    """
    if request.method == "POST":
        formulario = EdificioForm(request.POST)
        print(formulario.errors)

        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = EdificioForm()

    diccionario = {
        "formulario": formulario
    }

    return render(request, "crearEdificio.html", diccionario)


# Editar edificio
@login_required(login_url="/entrando/login/")
@permission_required("inmuebles.change_edificio", login_url="/entrando/login/")
def editar_edificio(request, id):
    """
    Permite editar un edificio.
    """
    edificio = Edificio.objects.get(pk=id)

    if request.method == "POST":
        formulario = EdificioForm(request.POST, instance=edificio)
        print(formulario.errors)

        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = EdificioForm(instance=edificio)

    diccionario = {
        "formulario": formulario
    }

    return render(request, "editarEdificio.html", diccionario)


# Eliminar edificio
@login_required(login_url="/entrando/login/")
@permission_required("inmuebles.delete_edificio", login_url="/entrando/login/")
def eliminar_edificio(request, id):
    """
    Permite eliminar un edificio.
    """
    edificio = Edificio.objects.get(pk=id)
    edificio.delete()

    return redirect(index)


# Crear departamento
@login_required(login_url="/entrando/login/")
@permission_required("inmuebles.add_departamento", login_url="/entrando/login/")
def crear_departamento(request):
    """
    Permite crear un departamento desde Django.
    """
    if request.method == "POST":
        formulario = DepartamentoForm(request.POST)
        print(formulario.errors)

        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = DepartamentoForm()

    diccionario = {
        "formulario": formulario
    }

    return render(request, "crearDepartamento.html", diccionario)


# Editar departamento
@login_required(login_url="/entrando/login/")
@permission_required("inmuebles.change_departamento", login_url="/entrando/login/")
def editar_departamento(request, id):
    """
    Permite editar un departamento.
    """
    departamento = Departamento.objects.get(pk=id)

    if request.method == "POST":
        formulario = DepartamentoForm(request.POST, instance=departamento)
        print(formulario.errors)

        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = DepartamentoForm(instance=departamento)

    diccionario = {
        "formulario": formulario
    }

    return render(request, "editarDepartamento.html", diccionario)


# Eliminar departamento
@login_required(login_url="/entrando/login/")
@permission_required("inmuebles.delete_departamento", login_url="/entrando/login/")
def eliminar_departamento(request, id):
    """
    Permite eliminar un departamento.
    """
    departamento = Departamento.objects.get(pk=id)
    departamento.delete()

    return redirect(index)


# ViewSets para Django REST Framework

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar usuarios.
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar grupos.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class EdificioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para listar, crear, editar y eliminar edificios.
    """
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para listar, crear, editar y eliminar departamentos.
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticated]