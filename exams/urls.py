from django.urls import path
from . import views

urlpatterns = [
    path('exam/<int:exam_id>/submit/', views.submit_exam, name='submit_exam'),
]