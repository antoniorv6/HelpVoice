import json
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.utils import resample

import numpy as np

# Leer datos
with open('./data/data.json', 'r') as f:
  data = json.load(f)

# Codificación Y (Diagnosticos)
lb = preprocessing.LabelBinarizer()
y = list(data.keys())
y = lb.fit_transform(y)

# Codificación X (Sintomas)
mlb = MultiLabelBinarizer()
X = list(data.values())
X = mlb.fit_transform(X)


# Entrenamos modelo        
clf = RandomForestClassifier(random_state=0)

clf.fit(X, y)


# Testeamos las predicciones

average_acc = np.array([]) # Accuracy medio
n_tests = 20 # Numero de pruebas

for i in range(n_tests):
  n_samples = 30
  success = 0

  samples = resample(list(data.keys()), n_samples=n_samples) # Se obtienen las muestras

  # Realizamos una prediccion con los sintomas de cada muestra
  for sample in samples:
    x = mlb.transform([data[sample]])
    pred = clf.predict(x)
    label = lb.inverse_transform(pred)

    if label == sample: 
     success+=1

  print("Iter",i,':' , round(success/n_samples, 2))
  average_acc = np.append(average_acc, [success/n_samples])

print('Average accuracy:', round(np.mean(average_acc),2))


# Para probar manualmente

"""

x = mlb.transform([{'diarrea'}])  # Se ponen aqui los síntomas

pred = clf.predict(x)

print(pred)
print(lb.inverse_transform(pred))

"""