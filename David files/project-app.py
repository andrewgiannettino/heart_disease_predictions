from flask import Flask, request, jsonify, render_template
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)

# Load the pre-trained ML model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize the SQLite database
def init_db():
    with sqlite3.connect('patients.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                hr INTEGER NOT NULL,
                prediction TEXT
            )
        ''')
        conn.commit()

# Insert a new patient record into the database
def add_patient(first_name, last_name, hr, prediction):
    with sqlite3.connect('patients.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (first_name, last_name, hr, prediction)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, hr, prediction))
        conn.commit()

# Route to display HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Control Panel Route
@app.route('/control_panel')
def control_panel():
    return render_template('control_panel.html')

# Function to predict using the loaded model
def predict_hr(hr):
    hr_array = np.array([[hr]])
    prediction = model.predict(hr_array)
    return prediction[0]

# Route to add patient and predict using the ML model
@app.route('/add_patient', methods=['POST'])
def add_patient_route():
    try:
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        hr = int(request.form['hr'])

        # add more features
        age = int(request.form['age'])
        cholesterol = int(request.form['cholesterol'])
        blood_pressure = int(request.form['blood pressure'])
        blood_sugar = int(request.form['blood sugar'])
        unnamed: 0 = int(request.form['unnamed: 0'])
        stress_level = int(request.form['stress level'])
        exercise_hours = int(request.form['exercise hours'])
        smoking_former = (request.form['smoking_former'])
        smoking_never = str(request.form['smoking_never'])
        alcohol_intake_moderate = str(request.form['alcohol intake_moderate'])
        obesity_yes = str(request.form['obesity_yes'])
        gender = str(request.form['gender_male'])
        chest_pain = str(request.form['chest pain type_non-anginal pain'])
        family_history = str(request.form['family history_yes'])
        exercise_induced = str(request.form['exercise induced angina_yes'])
        diabetes = str(request.form['diabetes_yes'])
        alcohol_intake = str(request.form['alcohol intake_none'])
        chest_pain_atype = str(request.form['chest pain type_atypical angina'])
        chest_pain_type = str(request.form['chest pain type_typical angina'])
        # Validation
        if not first_name or not last_name or hr <= 0:
            return jsonify({'error': 'Invalid input'}), 400
        
        # Use the heart rate to make a prediction using the ML model

        # turn the detailes into a daframe or a dictonary
        prediction = predict_hr(hr)
      
        
        # Insert patient data along with the prediction into the database
        add_patient(first_name, last_name, hr, prediction)
        return jsonify({'message': f'Patient added successfully! Prediction: {prediction}'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get all patients
@app.route('/patients', methods=['GET'])
def get_patients():
    try:
        with sqlite3.connect('patients.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM patients')
            patients = cursor.fetchall()
        return jsonify(patients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New route for cardiologists to see patient information and predictions
@app.route('/cardiologist', methods=['GET'])
def cardiologist():
    try:
        with sqlite3.connect('patients.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT first_name, last_name, hr, prediction FROM patients')
            patients = cursor.fetchall()
        return render_template('cardiologist.html', patients=patients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
