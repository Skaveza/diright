import pandas as pd
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# Load the data
data_path = os.path.join(os.path.dirname(__file__), 'medical_data.csv')
data = pd.read_csv(data_path)

# Prepare the features (X) and target (y)
X = data.drop('diagnosis', axis=1)
y = data['diagnosis']

# Encode categorical variables
le_dict = {}
for column in X.columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    le_dict[column] = le

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Save the model and encoder
joblib.dump(clf, 'model.pkl')
joblib.dump(le_dict, 'label_encoders.pkl')

# Function to predict diagnosis
def predict_diagnosis(symptoms, medical_history):
    # Load the model and encoder
    clf = joblib.load('model.pkl')
    le_dict = joblib.load('label_encoders.pkl')
    
    # Prepare the input data
    input_data = pd.DataFrame([symptoms + [medical_history]], columns=X.columns)
    
    # Encode the input data
    for column in input_data.columns:
        if column in le_dict:
            input_data[column] = le_dict[column].transform(input_data[column])
        else:
            raise ValueError(f"Column {column} not found in label encoders")
    
    # Make prediction
    diagnosis = clf.predict(input_data)
    return diagnosis[0]
