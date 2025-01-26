from django.contrib import admin
from .models import Medecin

class MedecinAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'specialite']  # Add specialite field if you have it
    search_fields = ['username', 'first_name', 'last_name', 'specialite']  # Search by extra fields like specialization
    ordering = ['id']

admin.site.register(Medecin, MedecinAdmin)
