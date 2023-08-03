import json
import numpy as np
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D # type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from sklearn.preprocessing import LabelEncoder
from keras import callbacks

from colors import prsys
# from colors import prsys


def training(mode, num_epochs, path):
    with open(str(path)+'/lessons.json') as file:
        data=json.load(file)

    sample_sentences=[]
    sample_labels=[]
    labels=[]
    responses=[]

    for sentence in data['lessons']:
        for q in sentence['questions']:
            sample_sentences.append(q)
            sample_labels.append(sentence['tag'])
        responses.append(sentence['responses'])
        if sentence['tag'] not in labels:
            labels.append(sentence['tag'])

    num_classes=len(labels)
    label_encoder=LabelEncoder()
    label_encoder.fit(sample_labels)
    sample_labels=label_encoder.transform(sample_labels)
    # print(sample_labels.shape, type(sample_labels))

    tokenizer=Tokenizer(num_words=1000,oov_token="<OOV>")
    tokenizer.fit_on_texts(sample_sentences)
    # word_index=tokenizer.word_index
    sequences=tokenizer.texts_to_sequences(sample_sentences)

    max_padding = 20
    padded_sequences=pad_sequences(sequences, truncating='post', maxlen=max_padding)
    # print(padded_sequences.shape, type(padded_sequences), padded_sequences)

    """neural network"""
    model=Sequential()
    max_input = 1000
    emb_dim = 16
    model.add(Embedding(max_input, emb_dim, input_length=max_padding))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(emb_dim, activation='relu'))
    model.add(Dense(emb_dim, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.summary()

    es = callbacks.EarlyStopping(monitor="loss", mode="min", min_delta=0.05, verbose=mode, patience=20, baseline=None, start_from_epoch=200)
    model.fit(padded_sequences, np.array(sample_labels), epochs=num_epochs, verbose=mode, callbacks=[es])
    # hist=model.fit(padded_sequences, np.array(sample_labels), epochs=num_epochs)
    v=(es.stopped_epoch if es.stopped_epoch>0 else num_epochs)

    return v, model, tokenizer, label_encoder

def start_training(mode, path, num):
    result=0
    # input(f"{num}: ")
    while num>=result:
        result, model, tokenizer, label_encoder=training(mode, num, path)
        if result!=num:
            if mode==1:
                prsys(f"Yummy! I ate {result} epochs!")
            model.save(str(path)+"/training")
            """save the tokenizer and encoder"""
            with open(str(path)+'/pickles/tokenizer.pickle', 'wb') as token:
                pickle.dump(tokenizer, token, protocol=pickle.HIGHEST_PROTOCOL)
            with open(str(path)+'/pickles/label_encoder.pickle', 'wb') as enc:
                pickle.dump(label_encoder, enc, protocol=pickle.HIGHEST_PROTOCOL)
            prsys("Training finished")
            epoch_upd=num
            break
        else:
            if mode==1:
                prsys(f"{result}: Need more epochs :(")
            num+=100
    return epoch_upd



# start_training(mode=0,path='classification_training/database/user',num=500) 

