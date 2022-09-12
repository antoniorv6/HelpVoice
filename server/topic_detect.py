import json
import torch
import pickle
from transformers import BertModel, BertTokenizerFast
from torch import nn
import nltk
nltk.download('stopwords')
sw_nltk = nltk.corpus.stopwords.words('spanish')

tokenizer = BertTokenizerFast.from_pretrained("setu4993/LaBSE")
model = BertModel.from_pretrained("setu4993/LaBSE")
model = model.eval()

cos = nn.CosineSimilarity(dim=1, eps=1e-6)


def getEmbeddings(inputs):

    inputs_tokens = tokenizer(inputs, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(**inputs_tokens)

    outputs = outputs.pooler_output

    return outputs

def uniqueList(lista):
    unique = [item for sublist in lista for item in sublist]
    unique = list(dict.fromkeys(unique))
    return unique

# Leer datos
with open('./data/data.json', 'r') as f:
  data = json.load(f)

# Obtener el embedding medio de todos los simtomas
symps = list(data.values())

symps_unique = uniqueList(symps)
symp_emb = getEmbeddings(symps_unique).mean(dim=0)

# tratamos de comparar ahora palabras para ver su nivel de similitud con el tema

text = "Me duele el pecho y tengo aritmia"

text = [word for word in text.split() if word.lower() not in sw_nltk]

interestig_words = []

for word in text:
    if cos(symp_emb, getEmbeddings([word])).tolist()[0] > 0.6:
        interestig_words.append(word)

print("Palabras interesnates detectadas", interestig_words)
# Cargamos modelo
knn_model = pickle.load(open('models/knn_model.sav', 'rb'))
lb = pickle.load(open('models/lb.sav', 'rb'))
pred = knn_model.predict(getEmbeddings(interestig_words))
label = lb.inverse_transform(pred)

print('Creo que tienes', label[0])




