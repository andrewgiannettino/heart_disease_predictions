from flask import Flask, render_template, request
import pandas as pd
from ml_model import predict

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get user input data from the form
        user_input = {
            'feature1': float(request.form['feature1']),
            'feature2': float(request.form['feature2']),
            # Add more features as necessary
        }

        # Convert to DataFrame (if needed for your model)
        user_df = pd.DataFrame([user_input])

        # Run the prediction
        prediction = predict(user_df)

        return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)