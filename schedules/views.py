from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from schedules.models import Schedule
from .serializers import ScheduleSerializer, ScheduleDoctorListSerializer
from .permissions import IsDoctor, IsDoctorOwner
from django.utils import timezone


class ScheduleView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def perform_create(self, serializer):
        date = serializer.validated_data["date"]
        hour = serializer.validated_data["hour"]
        date_now = timezone.now().date()
        hour_now = timezone.now().time()
        if date < date_now or date == date_now and hour < hour_now:
            raise ParseError("Incorrect Date or Hour! Date or Hour already expired!")
        serializer.save(doctor=self.request.user)


class ScheduleDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctorOwner]

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    lookup_url_kwarg = "schedule_id"

    def perform_update(self, serializer):
        if not self.request.user.is_doctor or self.request.user != self.get_object().doctor:
            serializer.validated_data.clear()
            if self.get_object().user is None and self.get_object().is_available:
                serializer.save(user=self.request.user, is_available=False)
            else:
                serializer.save(user=None, is_available=True)
        serializer.save()


class ScheduleListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)

    serializer_class = ScheduleSerializer


class ScheduleDoctorListView(ListAPIView):
    def get_queryset(self):
        return Schedule.objects.filter(doctor_id=self.kwargs["pk"])

    serializer_class = ScheduleDoctorListSerializer
