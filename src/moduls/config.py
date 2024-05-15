import os

class PipeConfig:
    def __init__(self):
        self.feature_file = "tfidf_features.txt"
        self.context_length = 40
        self._features = None
        # Define the base directory relative to the current file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.feature_folder = os.path.join(base_dir, "../output")

    def load_features(self):
        feature_file_path = os.path.join(self.feature_folder, self.feature_file)
        with open(feature_file_path, 'r') as f:
            feature_names = f.read().splitlines()
        return feature_names

    def get_features(self):
        if self._features is None:
            self._features = self.load_features()
        return self._features


