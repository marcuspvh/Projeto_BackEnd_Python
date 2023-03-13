from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from schedules.models import Schedule
from .serializers import UserSerializer
from .permissions import IsAccountOwnerOrAdmin, IsAdminListUsers


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminListUsers]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.validated_data["is_doctor"] = False
        serializer.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdmin]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        schedules = Schedule.objects.filter(user=self.request.user).first()
        schedules.user = None
        schedules.is_available = True
        schedules.save()
        instance.is_active = False
        instance.save()


class DoctorView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return User.objects.filter(is_doctor=True)
        return User.objects.all()

    def perform_create(self, serializer):
        is_doctor = serializer.validated_data.get("info_doctor", None)
        if is_doctor is None:
            raise ParseError("info_doctor is a required field.")
        serializer.save()


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAccountOwnerOrAdmin]

    serializer_class = UserSerializer

    def get_queryset(self):
        schedules = self.request.path
        if schedules == "schedules":
            return Schedule.objects.filter(doctor_id=self.kwargs["pk"])
        return User.objects.filter(is_doctor=True)

    def perform_destroy(self, instance):
        schedules = Schedule.objects.filter(doctor=self.request.user)
        schedules.delete()
        instance.is_active = False
        instance.save()
