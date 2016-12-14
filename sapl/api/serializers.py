from django.utils import formats
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from sapl.base.models import Autor
from sapl.materia.models import MateriaLegislativa
from sapl.parlamentares.models import SessaoLegislativa
from sapl.sessao.models import SessaoPlenaria, TipoSessaoPlenaria


class ChoiceSerializer(serializers.Serializer):
    value = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj[1]

    def get_value(self, obj):
        return obj[0]


class ModelChoiceSerializer(ChoiceSerializer):

    def get_text(self, obj):
        return str(obj)

    def get_value(self, obj):
        return obj.id


class ModelChoiceObjectRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return ModelChoiceSerializer(value).data


class AutorChoiceSerializer(ModelChoiceSerializer):

    def get_text(self, obj):
        return obj.nome

    class Meta:
        model = Autor
        fields = ['id', 'nome']


class AutorSerializer(serializers.ModelSerializer):
    autor_related = ModelChoiceObjectRelatedField(read_only=True)

    class Meta:
        model = Autor


class MateriaLegislativaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MateriaLegislativa
        fields = '__all__'


class TipoSessaoPlenariaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoSessaoPlenaria
        fields = '__all__'


class SessaoLegislativaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SessaoLegislativa
        fields = '__all__'


class TituloSessaoPlenariaField(serializers.Field):

    def to_representation(self, obj):
        return formats.date_format(obj, 'd/m/Y (l)')


class MobileSessaoPlenariaSerializer(serializers.ModelSerializer):
    tipo = TipoSessaoPlenariaSerializer(read_only=True)
    sessao_legislativa = SessaoLegislativaSerializer(read_only=True)
    data = TituloSessaoPlenariaField(source='data_inicio')

    class Meta:
        model = SessaoPlenaria
        fields = ('id',
                  'numero',
                  'tipo',
                  'sessao_legislativa',
                  'data',
                  'hora_inicio')
