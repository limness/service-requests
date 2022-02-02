
from datetime import timedelta

from rest_framework import serializers

from .models import User, DiagnosticRequest


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=128, min_length=8, write_only=True)
    car = serializers.CharField(max_length=16, min_length=2, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CarRegistrationSerializer(serializers.ModelSerializer):

    # expert = serializers.CharField(max_length=128, min_length=8, write_only=True)
    time = serializers.DateTimeField(write_only=True)

    def validate(self, data):
        # Проверяем на выходные
        if data['time'].weekday() == 6 or data['time'].weekday() == 5:
            raise serializers.ValidationError("Wow wow wow chill chill! It's weekend..")

        # Проверяем на рабочие часы (Работа с 10 до 22)
        # Из-за диагностики сгоняем диапозон на один час ближе
        if data['time'].hour < 10 or data['time'].hour > 20:
            raise serializers.ValidationError("Мы в эти часы не работаем. Запись осуществляется с 10:00 до 21:00")

        # Так как диагностика идет час, берем диапозон указаного времени
        # с +- часом и ищем существующие заявки на диагностику у двыбранного мастера
        expert_work_time = DiagnosticRequest.objects.filter(
            expert=data['expert'],
            time__range=[
                data['time'] - timedelta(hours=1),
                data['time'] + timedelta(hours=1)
            ]
        )
        # Ств если были найдены некоторые объекты, значит время уже занято
        if expert_work_time.count() > 0:
            raise serializers.ValidationError("Это время уже кем-то занято или чуть позже стоит другая запись, выбери другое время.")

        return data

    class Meta:
        model = DiagnosticRequest
        fields = ('__all__')

class UpdateFullNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('full_name',)

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.save()
        return instance

class UpdateCarSerializer(serializers.ModelSerializer):

   class Meta:
        model = User
        fields = ('car',)

   def update(self, instance, validated_data):
        instance.car = validated_data.get('car', instance.car)
        instance.save()
        return instance

class ExpertListSerializer(serializers.ModelSerializer):

   class Meta:
        model = User
        fields = ('id', 'full_name',)
