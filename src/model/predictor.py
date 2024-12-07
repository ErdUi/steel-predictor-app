import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

class SteelPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()

    def train(self, X, y):
        self.model = RandomForestRegressor(
            n_estimators=1000,
            max_depth=20,
            min_samples_split=4,
            min_samples_leaf=2,
            max_features='sqrt',
            bootstrap=True,
            random_state=42
        )
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, X):
        if self.model is None:
            raise ValueError('Model not trained')
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)