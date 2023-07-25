import json
import numpy as np
import pickle
from tensorflow.keras import models # type: ignore
from tensorflow.keras import preprocessing # type: ignore
from colors import prbot, prsys, insys

def lessons_length(path):
    with open(str(path)+'/lessons.json') as read:
        dataread = json.load(read)

    elem_count=0
    for elem in dataread['lessons']:
        elem_count+=1
    return elem_count

def learning_from_chat(path, name):
    elem_count = lessons_length(path)
    i=0
    j=1
    prsys("Entering learning mode...")
    while True:
        if i%2==0:
            prbot("Ask me a question.")
            inp1=input(f"{name}: ")
            if inp1.lower()=="exit":
                break
            i=i+1
        if i%2!=0:
            prbot("What should I answer?")
            inp2 = input(f"{name}: ")
            if inp2.lower()=="exit":
                break
            i=i+1
        append_to_json(j,elem_count,inp1,inp2,path)

def append_to_json(j,elem_count,inp1,inp2,path):
        data = {"tag":"lesson"+str(elem_count+j),"questions":[inp1],"responses":[inp2]}
        j=j+1
        with open(str(path)+'/lessons.json','r+') as file:
            filedata=json.load(file)
            filedata["lessons"].append(data)
            file.seek(0)
            json.dump(filedata, file)

def chatbot(name,path,mode):
    with open(str(path)+'/lessons.json') as intenstfile:
        data=json.load(intenstfile)
    model=models.load_model(str(path)+'/training')
    with open(str(path)+'/pickles/tokenizer.pickle', 'rb') as token:
        tokenizer = pickle.load(token)
    with open(str(path)+'/pickles/label_encoder.pickle', 'rb') as enc:
        label_encoder = pickle.load(enc)
    while True:
        inp=input(f"{name}: ")
        if inp.lower()=="exit":
            return inp

        res = model.predict(preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=20), verbose=0)[0]
        res_index=np.argmax(res)
        tag = label_encoder.inverse_transform([np.argmax(res)])
        # if mode==1:print(res, len(res), res_index, tag[0], res[res_index])
        if mode==1:prsys(f"Confidence: {res[res_index]}")
        # is_answer=0
        if res[res_index]>0.8: # TODO: calculate the threshold
            for i in data['lessons']:
                if i['tag']==tag:
                    prbot(np.random.choice(i['responses']))
                    # is_answer=1
                    # return inp, is_answer
        else:
            prbot("Give me a minute...")
            return inp
