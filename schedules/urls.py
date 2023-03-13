from django.urls import path

from . import views

urlpatterns = [
    path("schedules/", views.ScheduleView.as_view()),
    path("schedules/<int:schedule_id>/", views.ScheduleDetailView.as_view()),
    path("schedules/user/", views.ScheduleListView.as_view()),
]
