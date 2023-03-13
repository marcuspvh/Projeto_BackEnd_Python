from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Address, Doctor_specialties, Doctor_info
from schedules.models import Schedule


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class Doctor_specialtiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor_specialties
        fields = ["id", "name_specialties"]


class Doctor_infoSerializer(serializers.ModelSerializer):

    specialties = Doctor_specialtiesSerializer(many=True)

    class Meta:
        model = Doctor_info
        fields = ["id", "crm", "specialties"]


class UserListScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["id", "hour", "date", "type", "description", "doctor"]


class DoctorListScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["id", "hour", "date", "type", "description", "user"]


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="This field must be unique."
            ),
        ]
    )
    address = AddressSerializer()
    info_doctor = Doctor_infoSerializer(required=False)
    schedules = UserListScheduleSerializer(many=True, read_only=True)
    doctor_schedules = DoctorListScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "email",
            "password",
            "cpf",
            "age",
            "sex",
            "phone_number",
            "address",
            "schedules",
            "is_doctor",
            "info_doctor",
            "doctor_schedules",
            "is_superuser",
            "is_active",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        address_dict = validated_data.pop("address")
        is_superuser = validated_data["is_superuser"]
        is_doctor = validated_data["is_doctor"] or None

        address_obj = Address.objects.create(**address_dict)

        if is_doctor == False or is_doctor is None:
            if is_superuser == True:
                return User.objects.create_superuser(
                    **validated_data, address=address_obj
                )

            return User.objects.create_user(**validated_data, address=address_obj)

        if is_doctor == True:
            doctor_info_dict = validated_data.pop("info_doctor")
            doctor_specialties_list = doctor_info_dict.pop("specialties")

            if is_superuser == True:
                user_obj = User.objects.create_superuser(
                    **validated_data, address=address_obj
                )
                doctor_info_obj, _ = Doctor_info.objects.get_or_create(
                    **doctor_info_dict
                )

                for specialties in doctor_specialties_list:
                    (
                        doctor_specialties_obj,
                        _,
                    ) = Doctor_specialties.objects.get_or_create(**specialties)
                    doctor_info_obj.specialties.add(doctor_specialties_obj)

                user_obj.info_doctor = doctor_info_obj
                user_obj.save()

                return user_obj

            else:
                user_obj = User.objects.create_user(
                    **validated_data, address=address_obj
                )
                doctor_info_obj, _ = Doctor_info.objects.get_or_create(
                    **doctor_info_dict
                )

                for specialties in doctor_specialties_list:
                    (
                        doctor_specialties_obj,
                        _,
                    ) = Doctor_specialties.objects.get_or_create(**specialties)
                    doctor_info_obj.specialties.add(doctor_specialties_obj)

                user_obj.info_doctor = doctor_info_obj
                user_obj.save()

                return user_obj

    def update(self, instance: User, validated_data: dict) -> User:

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)

            elif key == "address":
                address_dict = validated_data["address"]
                address_key = address_dict.items()
                
                for key, value in address_key:
                    setattr(instance.address, key, value)
                instance.address.save()

            elif key == "info_doctor":
                info_doctor_dict = validated_data["info_doctor"]

                info_doctor_obj = info_doctor_dict.items()

                for key, value in info_doctor_obj:
                    if key == "crm":
                        instance.info_doctor.crm = info_doctor_dict["crm"]

                    elif key == "specialties":

                        new_spectialties_list = info_doctor_dict["specialties"]

                        for specialties in new_spectialties_list:
                            (
                                new_speciealties_obj,
                                _,
                            ) = Doctor_specialties.objects.get_or_create(**specialties)
                            info_doctor_instanc = Doctor_info.objects.get(
                                pk=instance.info_doctor.id
                            )
                            info_doctor_instanc.specialties.add(new_speciealties_obj)
                instance.info_doctor.save()

            else:
                setattr(instance, key, value)

        instance.save()

        return instance
