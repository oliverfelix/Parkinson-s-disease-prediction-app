import sys
from flask import Flask, render_template, redirect, request, url_for,session
import logging
import numpy as np
from Parkinson.pipeline.prediction import PredictionPipeline
from exception import customexception

app = Flask(__name__)


# Secret key for session management
app.secret_key = 'your_secret_key'

# Dictionary to store registered users' information
# Dictionary to store registered users' details
registered_users = {
    'user1': {'password': 'password1', 'fullname': 'User One'},
    'user2': {'password': 'password2', 'fullname': 'User Two'}
}
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



# @app.route('/', methods=['GET', 'POST'])
# def index():
#     error = None
#     if request.method == 'POST':
#         # Check if the form submission is for login or register
#         if 'login' in request.form:
#             # Attempt login
#             username = request.form['username']
#             password = request.form['password']
#             if username in registered_users and registered_users[username]['password'] == password:
#                 session['username'] = username
#                 return redirect(url_for('input'))  # Redirect to input.html after successful login
#             else:
#                 error = 'Invalid username or password'
#         elif 'register' in request.form:
#             # Register new user
#             username = request.form['username']
#             password = request.form['password']
#             fullname = request.form['fullname']
#             if username in registered_users:
#                 error = 'Username already exists. Please choose a different username.'
#             else:
#                 registered_users[username] = {'password': password, 'fullname': fullname}
#                 return redirect(url_for('index'))  # Redirect to index.html after successful registration
#     return render_template('index.html', error=error)

# @app.route('/input')
# def input():
#     # Render the input form for prediction
#     username = session.get('username')
#     if username:
#         return render_template('input.html', username=username)
#     else:
#         return redirect(url_for('index'))
    
    
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username exists and password is correct
        if username in registered_users and registered_users[username]['password'] == password:
            # Redirect to input page if login is successful
            return redirect(url_for('input'))
        else:
            # Render login page with error message
            return render_template('login.html', error='Wrong username or password. Please try again.')
    # Render login page for GET requests
    return render_template('login.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        # Check if username already exists
        if username in registered_users:
            # Render register page with error message
            return render_template('register.html', error='Username already exists. Please choose a different username.')
        else:
            # Add new user to registered_users dictionary
            registered_users[username] = {'password': password, 'fullname': fullname}
            # Redirect to home page after successful registration
            return redirect(url_for('index'))
    # Render register page for GET requests
    return render_template('register.html', error=None)

@app.route('/input')
def input():
    return render_template('input.html')



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
            raise customexception(e,sys)
            return 'Something went wrong. Check the logs for details.'

    else:
        # Render the prediction page
        return render_template('prediction.html')


# Route for Illness Ratio
@app.route('/illness_ratio', methods=['GET'])
def illness_ratio():
    # Logic for Illness Ratio
    return "Illness Ratio Page"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    print("Flask application running at http://127.0.0.1:8080")
