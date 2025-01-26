# Documentation du projet : PredictionSymptoms

## Vue d'ensemble
PredictionSymptoms est une application web alimentée par l'apprentissage automatique, conçue pour prédire des symptômes médicaux et fournir des informations aux utilisateurs en fonction des données saisies. Le projet intègre des modèles d'apprentissage automatique dans un cadre web basé sur Django.

## Structure du projet
Le projet est organisé comme suit :
```
PredictionSymptoms/
├── .git/               # Contrôle de version Git
├── accounts/           # Gestion des comptes utilisateurs
├── Data/               # Contient les jeux de données pour l'entraînement et les prédictions
├── db.sqlite3          # Base de données SQLite pour les données de l'application
├── env/                # Environnement virtuel Python
├── manage.py           # Script de gestion Django
├── PredictionSymptoms/ # Configuration principale de l'application Django
├── predictor/          # Modèles d'apprentissage automatique et logique
```

## Testé avec
Ce projet a été testé avec **Python 3.12.2**.

## Instructions d'installation
Pour exécuter le projet en local, suivez ces étapes :

1. **Cloner le dépôt** :
    ```bash
   git clone https://github.com/ismail01100/PredictionSymptoms.git
    ```
   ```bash
   cd PredictionSymptoms
   ```
   ```bash
   code .
   ```

2. **Configurer l'environnement virtuel** :
   ```bash
   python -m venv env
   source env/bin/activate  # Pour Linux/Mac
   env\Scripts\activate    # Pour Windows
   ```

3. **Installer les dépendances** :
   ```bash
   pip install Django joblib scikit-learn requests pandas google-api-python-client google-generativeai
   ```

4. **Exécuter les migrations de base de données** :
   ```bash
   python manage.py migrate
   ```

5. **Créer un utilisateur administrateur** :
   ```bash
   python manage.py createsuperuser
   ```
   - Entrez un nom d'utilisateur (par exemple, admin).
   - Fournissez une adresse e-mail.
   - Définissez un mot de passe (il vous sera demandé de le confirmer).

6. **Démarrer le serveur de développement** :
   ```bash
   python manage.py runserver
   ```

7. Accédez à l'application à l'adresse `http://127.0.0.1:8000/admin/` pour l'interface administrateur ou `http://127.0.0.1:8000` pour l'application principale.

---

## Flux de travail de l'apprentissage automatique

### 1. **Préparation des données** :
- Le dossier `Data/` contient des jeux de données utilisés pour l'entraînement et les tests des modèles.
- Assurez-vous que les données sont prétraitées avant l'entraînement. Cela inclut la gestion des valeurs manquantes, l'encodage des variables catégoriques et la mise à l'échelle des caractéristiques numériques.

### 2. **Modèle d'apprentissage automatique** :

#### Algorithme utilisé
- **Random Forest Classifier** : Cet algorithme est choisi pour sa robustesse et sa capacité à gérer des données avec des relations non linéaires.

#### Processus d'entraînement
- Division entraînement/test : **80%** pour l'entraînement, **20%** pour les tests.
- Optimisation des hyperparamètres : Utilisation de **Grid Search** pour trouver les meilleurs paramètres.
- Validation croisée : Réalisée avec **k=5** pour évaluer les performances du modèle sur différents sous-ensembles de données.

#### Évaluation des performances
- Métriques utilisées :
  - **Précision** : Mesure de la proportion de prédictions correctes parmi toutes les prédictions.
  - **Rappel** : Évalue la capacité du modèle à identifier correctement les cas positifs.
  - **F1-score** : Moyenne harmonique de la précision et du rappel, utile pour un équilibre entre les deux.
  - **ROC-AUC** : Aire sous la courbe ROC, indiquant la capacité du modèle à distinguer entre les classes.

### 3. **Intégration** :
- Les modèles entraînés sont intégrés dans l'application Django.
- Les points de terminaison de prédiction sont exposés via les vues dans le module `predictor`.

### 4. **Déploiement** :
- Déployez l'application sur une plateforme cloud (par exemple, AWS, Heroku ou Azure).
- Assurez-vous que le modèle est optimisé pour des prédictions en temps réel.

---

## Composants clés

### 1. **`accounts/`** :
Gère l'authentification des utilisateurs et la gestion des comptes.

### 2. **`predictor/`** :
Se concentre sur les aspects liés à l'apprentissage automatique, y compris :
- **Entraînement des modèles** : Scripts et notebooks pour entraîner les modèles.
- **Logique de prédiction** : Fonctions pour gérer les saisies utilisateur et fournir des prédictions.
- **Intégration API** : Expose des API RESTful pour l'interaction avec les modèles.

### 3. **`Data/`** :
Contient :
- Jeux de données d'entraînement.
- Jeux de données de test.
- Scripts de prétraitement des données.

### 4. **`manage.py`** :
Utilitaire en ligne de commande de Django pour les tâches administratives.

---

## Jeux de données
Le répertoire `Data/` inclut des jeux de données essentiels pour l'entraînement et l'évaluation des modèles. Assurez-vous de ce qui suit :
- **Qualité des données** : Vérifiez que les données sont propres et bien structurées.
- **Formats de fichiers** : Les formats couramment pris en charge incluent CSV, JSON ou Excel.
- **Attributs** : Les attributs clés incluent les symptômes des patients, les antécédents médicaux et les étiquettes diagnostiques. Chaque jeu de données est étiqueté pour un apprentissage supervisé.

---

## Traitement des données

### Étapes pour le traitement des données :
1. **Nettoyage des données** :
   - Supprimez les doublons et gérez les valeurs manquantes en utilisant l'imputation par la moyenne, la médiane ou le mode.
   - Identifiez et gérez les valeurs aberrantes à l'aide de méthodes statistiques.

2. **Encodage des caractéristiques** :
   - Convertissez les variables catégoriques en représentations numériques en utilisant l'encodage one-hot ou l'encodage d'étiquettes.

3. **Normalisation et mise à l'échelle** :
   - Normalisez les données pour garantir que les caractéristiques ont une moyenne de 0 et un écart type de 1.

4. **Division des données** :
   - Divisez le jeu de données en sous-ensembles d'entraînement, de validation et de test (par exemple, 70%-20%-10%).

5. **Ingénierie des caractéristiques** :
   - Créez de nouvelles caractéristiques basées sur les connaissances du domaine pour améliorer les performances du modèle.

6. **Enregistrement des données traitées** :
   - Enregistrez les jeux de données prétraités pour une réutilisation lors de la phase d'entraînement.

---

## Intégration du chatbot

### Vue d'ensemble
Le projet inclut un chatbot pour l'interaction avec les utilisateurs, alimenté par l'API Gemini. Le chatbot permet aux utilisateurs de poser des questions liées à la santé et de recevoir des informations basées sur les modèles entraînés.

### Caractéristiques clés
- **Traitement du langage naturel (NLP)** : Traite les requêtes des utilisateurs pour comprendre leur intention et leur contexte.
- **Prédictions en temps réel** : Utilise le modèle d'apprentissage automatique pour fournir des réponses basées sur les saisies des utilisateurs.
- **Clé API** : Le chatbot est intégré à l'API Gemini à l'aide d'une clé sécurisée pour l'authentification.

### Étapes d'intégration
1. **Configurer la clé API** :
   - Obtenez la clé API Gemini depuis le tableau de bord développeur.
   - Enregistrez-la dans le fichier `.env` pour un accès sécurisé :
     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

2. **Implémenter la logique du chatbot** :
   - Utilisez le module `predictor/chatbot.py` pour gérer les requêtes utilisateur et interagir avec l'API Gemini.

3. **Exposer des points de terminaison** :
   - Créez des points de terminaison API dans Django pour faciliter l'interaction avec le chatbot :
     ```python
     from predictor.chatbot import Chatbot

     def chatbot_response(request):
         user_input = request.GET.get('query')
         bot = Chatbot(api_key='your_api_key_here')
         response = bot.get_response(user_input)
         return JsonResponse({'response': response})
     ```

4. **Intégration frontend** :
   - Ajoutez une interface de chat à l'application web pour l'interaction avec les utilisateurs.
   - Utilisez JavaScript ou React pour une communication en temps réel avec l'API du chatbot.

---

## Utilisation

### Entraînement du modèle
1. Placez le jeu de données dans le dossier `Data/`.
2. Exécutez le script d'entraînement :
   ```bash
   python predictor/train_model.py
   ```
3. Le modèle entraîné sera enregistré dans le répertoire `predictor/models/`.

### Faire des prédictions
1. Démarrez le serveur Django :
   ```bash
   python manage.py runserver
   ```
2. Accédez à la page de prédiction et fournissez les saisies requises.
3. Visualisez les résultats prédits.

### Utiliser le chatbot
1. Accédez à l'interface du chatbot dans l'application.
2. Entrez une requête liée aux symptômes ou aux préoccupations de santé.
3. Recevez des réponses en temps réel alimentées par l'API Gemini et le modèle entraîné.

---

## Contributions
Nous accueillons les contributions pour améliorer le projet. Suivez ces étapes :

1. Forkez le dépôt.
2. Créez une nouvelle branche pour votre fonctionnalité ou correction de bogue.
3. Validez vos modifications avec des messages clairs.
4. Poussez les modifications vers votre dépôt forké.
5. Soumettez une pull request.

---

## Travaux futurs
- Améliorer les modèles d'apprentissage automatique pour une précision accrue.
- Ajouter la prise en charge de plus de jeux de données.
- Améliorer l'interface utilisateur pour une meilleure expérience utilisateur.
- Déployer l'application sur une plateforme évolutive.
- Étendre les capacités du chatbot avec une prise en charge multilingue.

---
