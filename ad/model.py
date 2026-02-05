import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

X = np.load("normal_usage.npy")

model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)   # 2% allowed anomalies

model.fit(X)

joblib.dump(model, "anomaly_model.pkl")
print("Model trained")
