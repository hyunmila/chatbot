import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D # type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from sklearn.preprocessing import LabelEncoder

with open('lessons.json') as file:
    data=json.load(file)
# with open('lessons.json') as read:
#     dataread = json.load(read)

def training():
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
    # for sentence1 in dataread['lessons']:
    #     for q1 in sentence1['questions']:
    #         sample_sentences.append(q1)
    #         sample_labels.append(sentence1['tag'])
    #     responses.append(sentence1['responses'])
    #     if sentence1['tag'] not in labels:
    #         labels.append(sentence1['tag'])


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
    num_epochs = 400
    model.fit(padded_sequences, np.array(sample_labels), epochs=num_epochs)

    # save the model
    model.save("bot_model")

    # save the tokenizer and encoder
    import pickle
    with open('tokenizer.pickle', 'wb') as token:
        pickle.dump(tokenizer, token, protocol=pickle.HIGHEST_PROTOCOL)
    with open('label_encoder.pickle', 'wb') as enc:
        pickle.dump(label_encoder, enc, protocol=pickle.HIGHEST_PROTOCOL)

training()