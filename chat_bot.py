import json
import numpy as np
import pickle
import os, sys
from tensorflow.keras import models # type: ignore
from tensorflow.keras import preprocessing # type: ignore
from train_from_chat import learning_from_chat
from training import training
# from multiprocessing import Process, freeze_support

# def restart():
#         print("restarting")
#         # os.execv(sys.executable, [os.path.basename(sys.executable)] + sys.argv)
#         sys.stdout.flush()
#         os.execv(sys.argv[0], sys.argv)

with open('lessons.json') as intenstfile:
    data=json.load(intenstfile)

name = "User"

training()
print("Chatbot loaded")
model=models.load_model('best_model.h5')

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

        
    
    res = model.predict(preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=20), verbose=0) 
    tag = label_encoder.inverse_transform([np.argmax(res)])

    for i in data['lessons']:
        if i['tag']==tag:
            print("Bot: ", np.random.choice(i['responses']))


# name=input("Enter your name or skip: ")
# if name=='skip':
#     name="User"
# print("Hello "+name+", start texting, type exit to stop.")



