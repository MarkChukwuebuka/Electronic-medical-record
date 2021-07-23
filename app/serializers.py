from rest_framework import serializers
from .models import *


class PatientSerializer(serializers.ModelSerializer):
    worker = serializers.ReadOnlyField(source='worker.worker.surname')


    class Meta:
        model = Patient
        fields = ('id', 'name', 'surname', 'gender', 'age', 'worker')