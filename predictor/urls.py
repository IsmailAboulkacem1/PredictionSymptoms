from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Welcome page
    path('predictSymptom/', views.predict_symptom, name='predict_symptom'),
     path('audit_logs/', views.audit_logs_view, name='audit_logs'),
]