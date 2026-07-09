from rest_framework import serializers
from inmuebles.models import Edificio, Departamento
from rest_framework import serializers

class EdificioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edificio
        fields = '__all__'


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'