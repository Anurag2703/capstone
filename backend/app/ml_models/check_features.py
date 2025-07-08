# Purpose: Check the feature names in the trained model
# This script loads the trained burnout model and prints the feature names used during training.
# Ensures that there is no mismatch between the model's expected features and the data being passed for predictions.




import joblib

model = joblib.load("burnout_model.joblib")
print(model.feature_names_in_)
