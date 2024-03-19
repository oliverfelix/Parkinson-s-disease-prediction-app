import logging
import os
import sys
from flask import Flask, render_template, redirect, request, url_for
import numpy as np

from Parkinson.pipeline.prediction import PredictionPipeline
from exception import customexception

app = Flask(__name__)

# Route for home page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Route for Bar Chart
@app.route('/bar_chart', methods=['GET'])
def bar_chart():
    # Logic for Bar Chart
    return "Bar Chart Page"

# Route for Line Chart
@app.route('/line_chart', methods=['GET'])
def line_chart():
    # Logic for Line Chart
    return "Line Chart Page"

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        # Check if username and password are correct
        # If correct, redirect to the prediction page
        return redirect(url_for('prediction.html'))
    else:
        # Render the login page
        return render_template('login.html')

@app.route('/prediction', methods=['GET'])
def prediction():
    # Render the prediction page
    return render_template('prediction.html')


@app.route('/train', methods=['GET'])
def training():
    os.system("python main.py")
    return "Training Successful"

@app.route('/predict', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            # Reading the inputs given by the user
            MDVP_Fo = float(request.form['MDVP_Fo'])
            MDVP_Fhi = float(request.form['MDVP_Fhi'])
            MDVP_Flo = float(request.form['MDVP_Flo'])
            MDVP_Jitter = float(request.form['MDVP_Jitter'])
            MDVP_Jitter_Abs = float(request.form['MDVP_Jitter_Abs'])
            MDVP_RAP = float(request.form['MDVP_RAP'])
            MDVP_PPQ = float(request.form['MDVP_PPQ'])
            Jitter_DDP = float(request.form['Jitter_DDP'])
            MDVP_Shimmer = float(request.form['MDVP_Shimmer'])
            MDVP_Shimmer_dB = float(request.form['MDVP_Shimmer_dB'])
            Shimmer_APQ3 = float(request.form['Shimmer_APQ3'])
            Shimmer_APQ5 = float(request.form['Shimmer_APQ5'])
            MDVP_APQ = float(request.form['MDVP_APQ'])
            Shimmer_DDA = float(request.form['Shimmer_DDA'])
            NHR = float(request.form['NHR'])
            HNR = float(request.form['HNR'])
            RPDE = float(request.form['RPDE'])
            DFA = float(request.form['DFA'])
            spread1 = float(request.form['spread1'])
            spread2 = float(request.form['spread2'])
            D2 = float(request.form['D2'])
            PPE = float(request.form['PPE'])
            
            # Remove the last two elements (name and status) from the data array
            data = [MDVP_Fo, MDVP_Fhi, MDVP_Flo, MDVP_Jitter, MDVP_Jitter_Abs,
                    MDVP_RAP, MDVP_PPQ, Jitter_DDP, MDVP_Shimmer, MDVP_Shimmer_dB,
                    Shimmer_APQ3, Shimmer_APQ5, MDVP_APQ, Shimmer_DDA, NHR,
                    HNR, RPDE, DFA, spread1, spread2, D2, PPE]
            data = np.array(data).reshape(1, 22)  # Reshape to a 2D array
            
            obj = PredictionPipeline()
            predict = obj.predict(data)

            # Log prediction result
            logging.info(f"Prediction successful. Result: {predict}")

            return render_template('results.html', prediction=str(predict))

        except Exception as e:
            # Log any exceptions
            logging.error(f'The Exception message is: {e}')
            raise customexception(e,sys)
            return 'Something went wrong. Check the logs for details.'

    else:
        return render_template('index.html')


# Route for Illness Ratio
@app.route('/illness_ratio', methods=['GET'])
def illness_ratio():
    # Logic for Illness Ratio
    return "Illness Ratio Page"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
