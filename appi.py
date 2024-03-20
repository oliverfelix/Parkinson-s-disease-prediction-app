import sys
from loggingg import logging
from flask import Flask, render_template, redirect, request, session, url_for
from exception import customexception  # Import for generating unique session IDs
import numpy as np
from Parkinson.pipeline.prediction import PredictionPipeline

app = Flask(__name__)

# Secret key for session signing (replace with a strong secret)
app.secret_key = 'your_secret_key'

# Dictionary to store user sessions
user_sessions = {}

registered_users = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in registered_users:
            # Store the username and password in the dictionary
            registered_users[username] = password
            return redirect(url_for('login'))
        else:
            return 'Username already exists. Please choose a different username.'
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        if username in registered_users and registered_users[username] == password:
            # If login is successful, redirect to input page
            return redirect(url_for('input'))
        else:
            return 'Invalid username or password. Please try again.'
    return render_template('login.html')


@app.route('/input')
def input():
    username = session.get('username')
    return render_template('input.html', username=username)


@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
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
            raise customexception(e, sys)
    # If the request method is not POST, render the prediction page
    return render_template('prediction.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
