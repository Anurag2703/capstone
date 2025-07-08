#   Purpose:
#       load/predict burnout risk





# -----------------------------------------
# 1. Imports.
# -----------------------------------------
import joblib
import numpy as np
import pandas as pd

model = joblib.load("app/ml_models/burnout_model.joblib")




# -----------------------------------------
# 2. API route for burnout prediction.
# -----------------------------------------
def predict_burnout_risk(login_freq, forum_activity, assignment_delay, missed_classes):
    """
        You may later align these to match actual features from the CSV,
        but this is a placeholder to call the new model.
    """
    
    X = np.array([[login_freq, forum_activity, assignment_delay, missed_classes]])
    cols = [
        "login_frequency",
        "forum_activity",
        "assignment_delay_days",
        "missed_classes"
    ]
    df = pd.DataFrame(X, columns=cols)

    pred = model.predict_proba(df)[0][1]
    risk_level = "high" if pred > 0.5 else "low"
    return pred, risk_level