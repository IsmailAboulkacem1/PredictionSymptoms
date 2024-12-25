from django.db import models

class Prediction(models.Model):
    user_name = models.CharField(max_length=100)
    symptoms = models.JSONField()
    predicted_disease = models.CharField(max_length=100)
    prediction_date = models.DateTimeField(auto_now_add=True)

class AuditLogs(models.Model):
    id_patient = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    genre = models.CharField(max_length=10)
    age = models.IntegerField()
    prediction = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.prediction}"