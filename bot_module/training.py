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

    # conversion into model understandable form
    label_encoder=LabelEncoder()
    label_encoder.fit(sample_labels)
    sample_labels=label_encoder.transform(sample_labels)


    # oov replaces out of the vocabulary words with a special token
    tokenizer=Tokenizer(num_words=1000,oov_token="<OOV>") # create a vocabulary with limited words
    tokenizer.fit_on_texts(sample_sentences) # update vocabulary based on sentences
    word_index=tokenizer.word_index # words indexes in vocabulary
    sequences=tokenizer.texts_to_sequences(sample_sentences) # transform texts into sequences of integers

    # transform list of integers into a 2D numpy array (num_samples, num_timesteps)
    max_padding = 20 # max len of all sequences that others will be 'cut' to
    padded_sequences=pad_sequences(sequences, truncating='post', maxlen=max_padding)

    # neural network
    model=Sequential()
    max_input = 1000
    emb_dim = 16
    model.add(Embedding(max_input, emb_dim, input_length=max_padding)) # turn positive indexes into a dense vectors of fixed size
    model.add(GlobalAveragePooling1D()) # create fixed-length vector for each example by averaging on the sequence dim
    model.add(Dense(16, activation='relu')) # implement the activation operation on the input and give an output of length 16
    model.add(Dense(16, activation='relu'))
    model.add(Dense(num_classes, activation='softmax')) # output layer with a result of length of labels (categories)

    # stochastic gradient descent for large models (adam), loss function for more than two labels
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.summary()

    # training the model
    es = callbacks.EarlyStopping(monitor="loss", mode="min", min_delta=0.05, verbose=mode, patience=20, baseline=None, start_from_epoch=200)
    # mc =  callbacks.ModelCheckpoint('best_model.h5', monitor='loss', verbose=0, save_best_only=True) # this actually gives worse results
    # num_epochs = 500
    model.fit(padded_sequences, np.array(sample_labels), epochs=num_epochs, verbose=mode, callbacks=[es])
    # hist=model.fit(padded_sequences, np.array(sample_labels), epochs=num_epochs)
    v=(es.stopped_epoch if es.stopped_epoch>0 else num_epochs)
    # save the model
    return v, model, tokenizer, label_encoder

def start_training(mode, path, num):
    # num=100
    result=0
    while num>=result:
        result, model, tokenizer, label_encoder=training(mode, num, path)
        if result!=num:
            if mode==1:
                print("Yummy! I ate ", result, " epochs <3")
            model.save(str(path)+"/training")
            # save the tokenizer and encoder
            with open(str(path)+'/pickles/tokenizer.pickle', 'wb') as token:
                pickle.dump(tokenizer, token, protocol=pickle.HIGHEST_PROTOCOL)
            with open(str(path)+'/pickles/label_encoder.pickle', 'wb') as enc:
                pickle.dump(label_encoder, enc, protocol=pickle.HIGHEST_PROTOCOL)
            print("Training finished")
            epoch_upd=num
            break
        else:
            if mode==1:
                print(result,": So hungry, need more epochs :(")
            num+=100
    return epoch_upd



# start_training(0) 

