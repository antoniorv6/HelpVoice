import json
import numpy as np
import torch
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.utils import resample
from transformers import BertModel, BertTokenizerFast
import pickle


tokenizer = BertTokenizerFast.from_pretrained("setu4993/LaBSE")
model = BertModel.from_pretrained("setu4993/LaBSE")
model = model.eval()


def getEmbeddings(inputs):

    inputs_tokens = tokenizer(inputs, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(**inputs_tokens)

    outputs = outputs.pooler_output

    return outputs.mean(dim=0).tolist()


def codifyX(sympthoms):
    output = []
    for x in sympthoms:
        output.append(getEmbeddings(x))

    return output


# Leer datos
with open('./data/data.json', 'r') as f:
  data = json.load(f)

# Codificación Y (Diagnosticos)
lb = preprocessing.LabelBinarizer()
y = list(data.keys())
y = lb.fit_transform(y)

pickle.dump(lb, open('models/lb.sav', 'wb'))

# Codificación X (Sintomas)

X = list(data.values())
X = codifyX(X)

# Entrenamos modelo        
clf = KNeighborsClassifier(n_neighbors=1)
clf.fit(X, y)

# Guardamos modelo
filename = 'models/knn_model.sav'
pickle.dump(clf, open(filename, 'wb'))


# Testeamos las predicciones

average_acc = np.array([]) # Accuracy medio
n_tests = 20 # Numero de pruebas

for i in range(n_tests):
  n_samples = 30
  success = 0

  samples = resample(list(data.keys()), n_samples=n_samples) # Se obtienen las muestras

  # Realizamos una prediccion con los sintomas de cada muestra
  for sample in samples:
    x = codifyX([data[sample]])
    pred = clf.predict(x)
    label = lb.inverse_transform(pred)

    if label == sample: 
     success+=1

  print("Iter",i,':' , round(success/n_samples, 2))
  average_acc = np.append(average_acc, [success/n_samples])

print('Average accuracy:', round(np.mean(average_acc),2))
