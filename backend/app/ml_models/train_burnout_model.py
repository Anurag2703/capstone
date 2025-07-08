import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# load your synthetic CSV
df = pd.read_csv("burnout_synthetic.xls")

# separate features & target
X = df.drop(columns=["burnout_risk"])
y = df["burnout_risk"]

# train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# RandomForest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# save
joblib.dump(clf, "burnout_model.joblib")

print("✅ Model trained and saved to burnout_model.joblib")
