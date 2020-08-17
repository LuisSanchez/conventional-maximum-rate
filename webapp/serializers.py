from rest_framework import serializers
from webapp.models import TMC


class TMCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMC
        fields = ['titulo', 'subtitulo', 'valor', 'fecha', 'tipo']
