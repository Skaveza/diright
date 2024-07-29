import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# First, let's assume we have a CSV file with medical data
# The CSV might look like this:
# symptom1,symptom2,symptom3,medical_history,diagnosis
# fever,cough,fatigue,heart_disease,flu
# headache,nausea,dizziness,none,migraine
# ...

# Load the data
data_path = os.path.join(os.path.dirname(__file__), 'medical_data.csv')
data = pd.read_csv('medical_data.csv')

# Prepare the features (X) and target (y)
X = data.drop('diagnosis', axis=1)
y = data['diagnosis']

# Encode categorical variables
le = LabelEncoder()
for column in X.columns:
    X[column] = le.fit_transform(X[column])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Function to predict diagnosis
def predict_diagnosis(symptoms, medical_history):
    # Prepare the input data
    input_data = pd.DataFrame([symptoms + [medical_history]], columns=X.columns)
    
    # Encode the input data
    for column in input_data.columns:
        input_data[column] = le.fit_transform(input_data[column])
    
    # Make prediction
    diagnosis = clf.predict(input_data)
    return diagnosis[0]

# Example usage
symptoms = ['fever', 'cough', 'fatigue']
medical_history = 'none'
diagnosis = predict_diagnosis(symptoms, medical_history)
print(f"Predicted diagnosis: {diagnosis}")