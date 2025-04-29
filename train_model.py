
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier

def train_model_if_needed(model_path):
    if not os.path.exists(model_path):
        data = {
            'Flow Duration': np.random.randint(1000, 100000, 1000),
            'Tot Fwd Pkts': np.random.randint(1, 100, 1000),
            'Tot Bwd Pkts': np.random.randint(1, 100, 1000),
            'Pkt Len Mean': np.random.uniform(20, 100, 1000),
            'Label': np.random.choice(['DDoS', 'PortScan', 'BruteForce', 'Botnet', 'Normal'], 1000)
        }
        df = pd.DataFrame(data)
        X = df.drop('Label', axis=1)
        y = df['Label']

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(model, model_path)
    else:
        model = joblib.load(model_path)
    return model
