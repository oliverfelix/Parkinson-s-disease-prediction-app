import base64
from io import BytesIO
import logging
from flask import Flask, render_template, redirect, request, session, url_for
from matplotlib import pyplot as plt
import numpy as np
from Parkinson.pipeline.prediction import PredictionPipeline

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG) 

# Secret key for session signing (replace with a strong secret)
app.secret_key = 'your_secret_key'

# Dictionary to store user sessions
user_sessions = {}

registered_users = {}


@app.route('/', methods=['GET'])
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


@app.route('/results')
def results():
    # Fetch prediction result from session
    prediction_result = session.get('prediction_result')
    
    print("Prediction Result:", prediction_result) 
    return render_template('results.html', prediction=prediction_result)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    
    # Fetch prediction result from session
    prediction_result = session.get('prediction_result')

    if request.method == 'POST':
        return redirect(url_for('results'))
    else:
        return redirect(url_for('results'))
# Add a route for the bar chart page
@app.route('/bar_chart')
def bar_chart():
    # Model accuracy data
    models = ['LogisticRegression', 'xgboost', 'SVC', 'KNeighborsClassifier']
    accuracies = [90.0, 96.67, 86.67, 83.33]

    # Render the template with model accuracy data
    return render_template('bar_chart.html', models=models, accuracies=accuracies)
import pandas as pd
from flask import send_file

# Route for downloading user details and prediction result as Excel
@app.route('/download_data')
def download_data():
    # Get the logged-in user's username from the session
    username = session.get('username')
    
    # Fetch prediction result from session
    prediction_result = session.get('prediction_result')
    
    # Create a DataFrame with user details and prediction result
    user_data = pd.DataFrame({'Username': [username], 'Prediction Result': [prediction_result]})
    
    # Save DataFrame as Excel file
    excel_filename = f'user_data_{username}.xlsx'
    user_data.to_excel(excel_filename, index=False)
    
    # Send the Excel file to the user for download
    return send_file(excel_filename, as_attachment=True)

# Add a route for the line chart page
@app.route('/line_chart')
def line_chart():
    # Model accuracy data
    models = ['LogisticRegression', 'xgboost', 'SVC', 'KNeighborsClassifier']
    accuracies = [90.0, 96.67, 86.67, 83.33]

    # Render the template with model accuracy data
    return render_template('line_chart.html', models=models, accuracies=accuracies)


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
            data = np.array(data).reshape(1,22) # Reshape to a 2D array
            
            obj = PredictionPipeline()
            
            predicted_value = obj.predict(data)
            print(predicted_value)
            logging.info(f"Prediction successful. Result: {predicted_value}")
            # Store prediction result in session
            session['prediction_result'] = predict

            return render_template('results.html', prediction=str(predicted_value))
            # Log prediction result
            
            
            # Store prediction result in session
            # session['prediction_result'] = predict

            # return redirect(url_for('results'))

        except Exception as e:
            # Log any exceptions
            logging.error(f'The Exception message is: {e}')
            raise e
    # If the request method is not POST, render the prediction page
    return render_template('prediction.html')
@app.route('/illness_ratio', methods=['GET'])
def illness_ratio():
    # Example data: You should replace this with your actual data retrieval code
    affected_users = 70
    non_affected_users = 30

    # Create pie chart
    labels = ['Affected Users', 'Non-Affected Users']
    sizes = [affected_users, non_affected_users]
    colors = ['#ff9999', '#66b3ff']
    plt.figure(figsize=(7, 5))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Save the plot to a bytes object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the bytes object to base64 and render it in HTML
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('illness_ratio.html', plot_url=plot_url)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
