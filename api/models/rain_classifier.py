import pickle
from sklearn.preprocessing import MinMaxScaler


class RainClassifier:
    def __init__(self):
        self.classifier = pickle.load(open('trained_models/rainKNN.pkl', 'rb'))
        self.scaler = MinMaxScaler()

    def scale_data(self, weather_data):
        return self.scaler.fit_transform(weather_data)

    def classify(self, weather_data):
        scaled_data = self.scale_data(weather_data)
        return self.classifier.predict(scaled_data)
