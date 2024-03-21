# Importing the PredictionPipeline class from prediction.py
from src.Parkinson.pipeline.prediction import PredictionPipeline
import numpy as np

# Creating an instance of the PredictionPipeline class
pipeline = PredictionPipeline()

# Assuming you have new data stored in a NumPy array called new_data
new_data = np.array([[119.992,157.302,74.997,0.00784,0.00007,0.0037,0.00554,0.01109,
                             0.04374,0.426,0.02182,0.0313,0.02971,0.06545,0.02211,21.033,
                             0.414783,0.815285,-4.813031,0.266482,2.301442,0.284654]])  # Add values for each feature

# M # Replace ... with the rest of your data

# Making predictions using the predict method
predictions = pipeline.predict(new_data)

# Print or use the predictions as needed
print("Predictions:", predictions)
