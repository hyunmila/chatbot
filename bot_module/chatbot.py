import json
import numpy as np
import pickle
import sys
import time
from tensorflow.keras import models # type: ignore
from tensorflow.keras import preprocessing # type: ignore

def lessons_length(path):
    with open(str(path)+'/lessons.json') as read:
        dataread = json.load(read)

    elem_count=0
    for elem in dataread['lessons']:
        elem_count+=1
    return elem_count

def learning_from_chat(path):
    
    elem_count = lessons_length(path)
    i=0
    j=1
    print("Entering learning mode...")
    while True:

        if i%2==0:
            print("Bot: Ask me a question.")
            print("User: ", end="")
            inp1 = input()
            if inp1.lower()=="exit":
                break
            i=i+1
        if i%2!=0:
            print("Bot: What should I answer?")
            print("User: ", end="")
            inp2 = input()
            if inp2.lower()=="exit":
                break
            i=i+1
        
        
        data = {"tag":"lesson"+str(elem_count+j),"questions":[inp1],"responses":[inp2]}
        j=j+1
        with open(str(path)+'/lessons.json','r+') as file:
            filedata=json.load(file)
            filedata["lessons"].append(data)
            file.seek(0)
            json.dump(filedata, file)

def chatbot(name,path):

    with open(str(path)+'/lessons.json') as intenstfile:
        data=json.load(intenstfile)

    model=models.load_model(str(path)+'/training')

    with open(str(path)+'/pickles/tokenizer.pickle', 'rb') as token:
        tokenizer = pickle.load(token)

    with open(str(path)+'/pickles/label_encoder.pickle', 'rb') as enc:
        label_encoder = pickle.load(enc)

    print("Chatbot loaded")
    time.sleep(1)
    print("Hello "+name+", start texting, type exit to stop, learning to learn.")
    while True:
        print(name+": ", end="")
        inp = input()
        if inp.lower()=="exit":
            time.sleep(1)
            sys.exit("...Quitting...")
        if inp.lower()=="learning":
            time.sleep(1)
            learning_from_chat(path)
            break

        res = model.predict(preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=20), verbose=0) 
        tag = label_encoder.inverse_transform([np.argmax(res)])

        for i in data['lessons']:
            if i['tag']==tag:
                print("Bot: ", np.random.choice(i['responses']))
