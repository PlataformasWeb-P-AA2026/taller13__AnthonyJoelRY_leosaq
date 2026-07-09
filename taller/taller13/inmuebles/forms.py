from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

from inmuebles.models import Edificio, Departamento


class EdificioForm(ModelForm):
    class Meta:
        model = Edificio
        fields = ['nombre', 'direccion', 'ciudad', 'tipo']
        labels = {
            'nombre': _('Ingrese nombre del edificio'),
            'direccion': _('Ingrese dirección del edificio'),
            'ciudad': _('Ingrese ciudad'),
            'tipo': _('Seleccione tipo de edificio'),
        }

    def clean_nombre(self):
        valor = self.cleaned_data['nombre']

        if len(valor.strip()) < 3:
            raise forms.ValidationError("Ingrese un nombre de edificio válido")

        return valor

    def clean_direccion(self):
        valor = self.cleaned_data['direccion']

        if len(valor.strip()) < 5:
            raise forms.ValidationError("Ingrese una dirección más completa")

        return valor

    def clean_ciudad(self):
        valor = self.cleaned_data['ciudad']

        if len(valor.strip()) < 3:
            raise forms.ValidationError("Ingrese una ciudad válida")

        return valor


class DepartamentoForm(ModelForm):
    class Meta:
        model = Departamento
        fields = [
            'nombre_completo_propietario',
            'costo_departamento',
            'numero_cuartos',
            'edificio',
        ]
        labels = {
            'nombre_completo_propietario': _('Ingrese nombre completo del propietario'),
            'costo_departamento': _('Ingrese costo del departamento'),
            'numero_cuartos': _('Ingrese número de cuartos'),
            'edificio': _('Seleccione edificio'),
        }

    def clean_nombre_completo_propietario(self):
        valor = self.cleaned_data['nombre_completo_propietario']
        num_palabras = len(valor.split())

        if num_palabras < 2:
            raise forms.ValidationError("Ingrese el nombre completo del propietario")

        return valor

    def clean_costo_departamento(self):
        valor = self.cleaned_data['costo_departamento']

        if valor <= 0:
            raise forms.ValidationError("El costo del departamento debe ser mayor a 0")

        return valor

    def clean_numero_cuartos(self):
        valor = self.cleaned_data['numero_cuartos']

        if valor <= 0:
            raise forms.ValidationError("El número de cuartos debe ser mayor a 0")

        return valor


class DepartamentoEdificioForm(ModelForm):

    def __init__(self, edificio, *args, **kwargs):
        super(DepartamentoEdificioForm, self).__init__(*args, **kwargs)
        self.initial['edificio'] = edificio
        self.fields["edificio"].widget = forms.widgets.HiddenInput()
        print(edificio)

    class Meta:
        model = Departamento
        fields = [
            'nombre_completo_propietario',
            'costo_departamento',
            'numero_cuartos',
            'edificio',
        ]
        labels = {
            'nombre_completo_propietario': _('Ingrese nombre completo del propietario'),
            'costo_departamento': _('Ingrese costo del departamento'),
            'numero_cuartos': _('Ingrese número de cuartos'),
            'edificio': _('Edificio'),
        }