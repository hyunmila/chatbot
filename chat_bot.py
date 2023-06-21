import json
import numpy as np
import random
import pickle
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder


with open('intents.json') as file:
    data=json.load(file)

def chatbot():
    model=keras.models.load_model('bot_model')

    with open('tokenizer.pickle', 'rb') as token:
        tokenizer = pickle.load(token)

    with open('label_encoder.pickle', 'rb') as enc:
        label_encoder = pickle.load(enc)

    while True:
        try:
            print(name+":", end="")
            inp = input()
            if inp.lower()=="exit":
                break
            res = model.predict(keras.preprocessing.sequence.pad_sequences(
                tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=20))
            tag = label_encoder.inverse_transform([np.argmax(res)])

            for i in data['intents']:
                if i['tag']==tag:
                    print("Bot: ", np.random.choice(i['responses']))
        except:
            print("I'm sorry but I don't now the answer.")

name=input("Enter your name: ")
print("Hello "+name+", start texting, type exit to stop.")

chatbot()