import json


class Identification:

    def __init__(self):
        self.test_case = "FeatureTest.java"
        self.features = "features.json"

    def parse(self):
        with open(self.test_case) as f:
            features = {}
            sequence = []
            for line in f.readlines():
                if line.strip().startswith("//"):
                    print(line.strip())
                    if "Feature" in line:
                        features[line.strip().replace("// Feature: ", "")] = sequence
                        sequence = []
                        continue
                    elif "BACK" in line:
                        continue
                    sequence.append(line.strip())
        return features

    def save_features(self):
        with open(self.features, "w") as f:
            json.dump(self.parse(), f, indent=4, sort_keys=True)


if __name__ == '__main__':
    identify = Identification()
    identify.save_features()
