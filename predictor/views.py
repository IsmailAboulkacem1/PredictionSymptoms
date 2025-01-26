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





from django.contrib.auth.decorators import login_required
# View for predicting disease from symptoms
@login_required
def predict_symptom(request):
    # Retrieve patient data from the session
    patient_data = request.session.get('patient_data')
    if not patient_data:
        # Redirect to home if patient information is missing
        return redirect('home')

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

        # Log the prediction in the database
        AuditLogs.objects.create(
            id_patient=patient_data.get('id_patient'),
            nom=patient_data.get('nom'),
            prenom=patient_data.get('prenom'),
            genre=patient_data.get('genre'),
            age=patient_data.get('age'),
            prediction=prediction
        )

        # Render the result page with prediction
        return render(request, 'predictor/result.html', {
            'prediction': prediction,
            'patient_data': patient_data
        })

    # Render the symptom input form for GET requests
    return render(request, 'predictor/predict_symptom.html', {'patient_data': patient_data})


##############################################
from django.shortcuts import render
from .models import AuditLogs
def audit_logs_view(request):
    logs = AuditLogs.objects.all().order_by('-created_at')  # Fetch and order logs by creation date
    return render(request, 'predictor/audit_logs.html', {'logs': logs})


# Home Page#######################################################################""
# Home Page
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.method == 'POST':
        # Collect patient information from the form and save it to the session
        patient_data = {
            'id_patient': request.POST.get('id_patient'),
            'nom': request.POST.get('nom'),
            'prenom': request.POST.get('prenom'),
            'genre': request.POST.get('genre'),
            'age': request.POST.get('age'),
        }
        request.session['patient_data'] = patient_data
        # Clear the patient data from the session to reset the form
        #request.session.pop('patient_data', None)
        # Stay on the home page after saving the session
        return redirect('home')
    
    # Retrieve patient data from the session (if any)
    patient_data = request.session.get('patient_data', {})
    return render(request, 'predictor/home.html', {'patient_data': patient_data})



#chatbot
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import AuditLogs
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import os
import re
from django.shortcuts import render
from .models import AuditLogs
import re
import requests
import google.generativeai as genai
from django.shortcuts import render
from django.http import HttpResponse
# Configure the API key for Gemini
genai.configure(api_key="AIzaSyDyu3llPVZIDRUbJSzgBXNhwOfsr6JljDQ")

def chatbot_view(request):
    # Récupérer les données de la conversation depuis la session
    conversation_context = request.session.get('conversation_context', {
        'symptoms_collected': {},  # Symptômes collectés
        'dialogue_history': []    # Historique des questions/réponses
    })

    if request.method == 'POST':
        # Récupérer la réponse utilisateur depuis le formulaire
        user_response = request.POST.get('user_response', '')
        
        # Ajouter la réponse utilisateur à l'historique
        conversation_context['dialogue_history'].append({'role': 'user', 'content': user_response})

        # Collecter les symptômes en fonction de la réponse utilisateur
        keywords_to_symptoms = {
            "fatigue": "fatigue",
            "vomissement": "vomiting",
            "fièvre": "high_fever",
            "maux de tête": "headache",
            "douleur abdominale": "abdominal_pain",
        }
        for keyword, symptom_key in keywords_to_symptoms.items():
            if keyword in user_response.lower():
                conversation_context['symptoms_collected'][symptom_key] = 1

        # Générer une nouvelle question via Gemini
        dialogue_history = conversation_context['dialogue_history']
        prompt = f"""
        Voici le contexte de la conversation :
        {dialogue_history}.
        Symptômes collectés jusqu'à présent : {conversation_context['symptoms_collected']}.
        Continue la discussion en posant une question pour affiner la collecte des symptômes.
        """

        # Faire appel à l'API Gemini pour générer la réponse
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response:
            bot_question = response.text.strip()
        else:
            bot_question = "Je n'ai pas pu obtenir une réponse. Essayons une autre question."

        # Ajouter la question générée à l'historique
        conversation_context['dialogue_history'].append({'role': 'assistant', 'content': bot_question})

        # Mettre à jour le contexte de la conversation dans la session
        request.session['conversation_context'] = conversation_context

        # Retourner la question générée à l'utilisateur
        return render(request, 'predictor/chatbot.html', {
            'bot_question': bot_question,
            'dialogue_history': conversation_context['dialogue_history']
        })

    # Initialiser la conversation pour la méthode GET
    prompt = "Commence une discussion pour identifier des symptômes médicaux courants."

    # Faire appel à l'API Gemini pour démarrer la conversation
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    if response:
        bot_question = response.text.strip()
    else:
        bot_question = "Je n'ai pas pu obtenir une réponse. Essayons une autre question."

    # Enregistrer la première question dans l'historique
    conversation_context['dialogue_history'].append({'role': 'assistant', 'content': bot_question})
    request.session['conversation_context'] = conversation_context

    return render(request, 'predictor/chatbot.html', {
        'bot_question': bot_question,
        'dialogue_history': conversation_context['dialogue_history']
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def clear_chat(request):
    if request.method == 'POST':
        # Logique pour effacer l'historique (si stocké dans la base de données ou une session)
        request.session['dialogue_history'] = []  # Exemple : vider l'historique dans la session
        return JsonResponse({'success': True, 'message': 'Historique effacé avec succès.'})
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})
