import json
import numpy as np
import random
import pickle
from tensorflow import keras
from train_from_chat import learning_from_chat
# from sklearn.preprocessing import LabelEncoder


with open('lessons.json') as intenstfile:
    data=json.load(intenstfile)


def chatbot():
    model=keras.models.load_model('bot_model')

    with open('tokenizer.pickle', 'rb') as token:
        tokenizer = pickle.load(token)

    with open('label_encoder.pickle', 'rb') as enc:
        label_encoder = pickle.load(enc)

    while True:
        print(name+": ", end="")
        inp = input()
        if inp.lower()=="exit":
            break
        if inp.lower()=="learning":
            learning_from_chat()
        res = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=20)) # type: ignore
        tag = label_encoder.inverse_transform([np.argmax(res)])

        for i in data['lessons']:
            if i['tag']==tag:
                print("Bot: ", np.random.choice(i['responses']))


name=input("Enter your name or skip: ")
if name=='skip':
    name="User"
print("Hello "+name+", start texting, type exit to stop.")

chatbot()