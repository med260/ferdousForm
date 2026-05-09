from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('teacher/', views.teacher_form, name='teacher_form'),

    path(
        'students/<int:count>/',
        views.students_form,
        name='students_form'
    ),

    path(
        'success/<str:t_id>/',
        views.success_view,
        name='success_view'
    ),
]