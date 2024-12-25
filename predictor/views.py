from django.shortcuts import render
import os
import joblib

# Define BASE_DIR and model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "saved_model", "disease_prediction_model.pkl")

# Load the trained model
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please ensure the file exists.")

# View for predicting disease from symptoms
def predict_symptom(request):
    if request.method == 'POST':
        # Collect symptom inputs from the form
        symptoms = [
            int(request.POST.get('fatigue', 0)),
            int(request.POST.get('vomiting', 0)),
            int(request.POST.get('high_fever', 0)),
            int(request.POST.get('loss_of_appetite', 0)),
            int(request.POST.get('nausea', 0)),
            int(request.POST.get('headache', 0)),
            int(request.POST.get('abdominal_pain', 0)),
            int(request.POST.get('yellowish_skin', 0)),
            int(request.POST.get('yellowing_of_eyes', 0)),
            int(request.POST.get('chills', 0)),
            int(request.POST.get('malaise', 0)),
            int(request.POST.get('chest_pain', 0)),
            int(request.POST.get('muscle_pain', 0)),
            int(request.POST.get('phlegm', 0)),
            int(request.POST.get('cough', 0)),
        ]
        
        # Predict disease using the model
        prediction = model.predict([symptoms])[0]
        return render(request, 'predictor/result.html', {'prediction': prediction})
    
    # Render the symptom input form for GET requests
    return render(request, 'predictor/predict_symptom.html')

##############################################
from django.shortcuts import render
from .models import AuditLogs
def audit_logs_view(request):
    # Fetch all records from the AuditLogs table
    logs = AuditLogs.objects.all()
    return render(request, 'predictor/audit_logs.html', {'logs': logs})

# Home Page
def home(request):
    return render(request, 'predictor/home.html')