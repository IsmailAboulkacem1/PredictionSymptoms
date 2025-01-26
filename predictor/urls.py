from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    #path('save_patient_info/', views.save_patient_info, name='save_patient_info'),
    path('predictSymptom/', views.predict_symptom, name='predict_symptom'),
    path('audit_logs/', views.audit_logs_view, name='audit_logs'),
    path('chatbot/', views.chatbot_view, name='chatbot'),  # Chatbot avec formulaire
    path('chatbot/clear/', views.clear_chat, name='clear_chat'),

]
