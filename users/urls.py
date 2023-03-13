from django.urls import path
from . import views
from schedules import views as schedules_views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
    path("doctors/", views.DoctorView.as_view()),
    path("doctors/<int:pk>/", views.DoctorDetailView.as_view()),
    path("doctors/<int:pk>/schedules/", schedules_views.ScheduleDoctorListView.as_view()),
    path("users/login/", jwt_views.TokenObtainPairView.as_view()),
]
