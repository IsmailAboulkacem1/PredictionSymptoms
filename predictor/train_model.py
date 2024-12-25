import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Define paths for dataset and saving the model
data_path = r"C:\Users\HP\Desktop\PredictionSymptoms\Data\Balanced_Reduced_Dataset.csv"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_save_path = r"C:\Users\HP\Desktop\PredictionSymptoms\predictor\saved_model\disease_prediction_model.pkl"

# Load dataset
data = pd.read_csv(data_path)

# Drop unnecessary columns and prepare features and target
data_cleaned = data.drop(columns=['Unnamed: 0'])
X = data_cleaned.drop(columns=['prognosis'])
y = data_cleaned['prognosis']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Save the trained model
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
joblib.dump(clf, model_save_path)

print(f"Model trained and saved at {model_save_path}")
