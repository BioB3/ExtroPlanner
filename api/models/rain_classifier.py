import pickle
from sklearn.preprocessing import MinMaxScaler
import os


class RainClassifier:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(current_dir, "trained_models", "rainKNN.pkl")
        self.classifier = pickle.load(open(model_dir, "rb"))
        self.scaler = MinMaxScaler()

    def scale_data(self, weather_data):
        return self.scaler.fit_transform(weather_data)

    def classify(self, weather_data):
        scaled_data = self.scale_data(weather_data)
        return self.classifier.predict(scaled_data)
