from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

Medecin = get_user_model()

class MedecinRegisterForm(UserCreationForm):
    class Meta:
        model = Medecin
        fields = ['username', 'first_name', 'last_name', 'specialite', 'password1', 'password2']

class MedecinLoginForm(AuthenticationForm):
    class Meta:
        model = Medecin
        fields = ['username', 'password']
