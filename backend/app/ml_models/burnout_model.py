# burnout_model.py

# -----------------------------------------
# 1. Imports.
# -----------------------------------------
import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# -----------------------------------------
# 2. Load Model (Safe path)
# -----------------------------------------
model_path = os.path.join(os.path.dirname(__file__), "burnout_model.joblib")
model = joblib.load(model_path)

# -----------------------------------------
# 3. FastAPI App Init
# -----------------------------------------
app = FastAPI()

# -----------------------------------------
# 4. Input Schema
# -----------------------------------------
class BurnoutInput(BaseModel):
    login_freq: float
    forum_activity: float
    assignment_delay: float
    missed_classes: float

# -----------------------------------------
# 5. Burnout Prediction Function
# -----------------------------------------
def predict_burnout_risk(login_freq, forum_activity, assignment_delay, missed_classes):
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

# -----------------------------------------
# 6. API Route
# -----------------------------------------
@app.post("/burnout/")
def burnout_route(payload: BurnoutInput):
    prob, risk = predict_burnout_risk(
        payload.login_freq,
        payload.forum_activity,
        payload.assignment_delay,
        payload.missed_classes
    )
    return {
        "burnout_probability": round(prob, 4),
        "burnout_level": risk
    }







# #   Purpose:
# #       load/predict burnout risk





# # -----------------------------------------
# # 1. Imports.
# # -----------------------------------------
# import joblib
# import numpy as np
# import pandas as pd
# import os

# model_path = os.path.join(os.path.dirname(__file__), "burnout_model.joblib")
# model = joblib.load(model_path)

# # model = joblib.load("app/ml_models/burnout_model.joblib")




# # -----------------------------------------
# # 2. API route for burnout prediction.
# # -----------------------------------------
# def predict_burnout_risk(login_freq, forum_activity, assignment_delay, missed_classes):
#     """
#         You may later align these to match actual features from the CSV,
#         but this is a placeholder to call the new model.
#     """
    
#     X = np.array([[login_freq, forum_activity, assignment_delay, missed_classes]])
#     cols = [
#         "login_frequency",
#         "forum_activity",
#         "assignment_delay_days",
#         "missed_classes"
#     ]
#     df = pd.DataFrame(X, columns=cols)

#     pred = model.predict_proba(df)[0][1]
#     risk_level = "high" if pred > 0.5 else "low"
#     return pred, risk_level