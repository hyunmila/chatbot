import json
import numpy as np
import pickle
import sys
import time
from tensorflow.keras import models # type: ignore
from tensorflow.keras import preprocessing # type: ignore
from train_from_chat import learning_from_chat



def chatbot(name):

    with open('lessons.json') as intenstfile:
        data=json.load(intenstfile)

    model=models.load_model('bot_model')

    with open('tokenizer.pickle', 'rb') as token:
        tokenizer = pickle.load(token)

    with open('label_encoder.pickle', 'rb') as enc:
        label_encoder = pickle.load(enc)

    print("Chatbot loaded")
    while True:
        print(name+": ", end="")
        inp = input()
        if inp.lower()=="exit":
            time.sleep(2)
            sys.exit("...Quitting...")
        if inp.lower()=="learning":
            learning_from_chat()
            break

        res = model.predict(preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=20), verbose=0) 
        tag = label_encoder.inverse_transform([np.argmax(res)])

        for i in data['lessons']:
            if i['tag']==tag:
                print("Bot: ", np.random.choice(i['responses']))


# name=input("Enter your name or skip: ")
# if name=='skip':
#     name="User"
# print("Hello "+name+", start texting, type exit to stop.")



