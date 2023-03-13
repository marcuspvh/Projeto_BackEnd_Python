from rest_framework import serializers
from schedules.models import Schedule
from users.models import User
from users.serializers import AddressSerializer, Doctor_infoSerializer


class UserScheduleSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "email",
            "cpf",
            "age",
            "sex",
            "phone_number",
            "address",
            "is_active",
        ]


class DoctorScheduleSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    info_doctor = Doctor_infoSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "email",
            "cpf",
            "age",
            "sex",
            "phone_number",
            "is_doctor",
            "address",
            "is_active",
            "info_doctor",
        ]


class ScheduleDoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorScheduleSerializer(read_only=True)
    user = UserScheduleSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = "__all__"
