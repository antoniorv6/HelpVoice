import json
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.preprocessing import MultiLabelBinarizer

class DiseasePredictor():
    def __init__(self) -> None:
        with open('data/data.json', 'r') as f:
            data = json.load(f)
        
        self.lb = preprocessing.LabelBinarizer()
        y = list(data.keys())
        y = self.lb.fit_transform(y)

        # Codificación X (Sintomas)
        self.mlb = MultiLabelBinarizer()
        X = list(data.values())
        X = self.mlb.fit_transform(X)
        # Entrenamos modelo        
        self.clf = RandomForestClassifier(random_state=0)
        self.clf.fit(X, y)

    
    def __call__(self, symptomList):
        x = self.mlb.transform(symptomList)
        pred = self.clf.predict(x)
        label = self.lb.inverse_transform(pred)
        return label