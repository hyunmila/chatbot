import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D # type: ignore
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from sklearn.preprocessing import LabelEncoder

with open('intents.json') as file:
    data=json.load(file)

sample_sentences=[]
sample_labels=[]
labels=[]
responses=[]

for sentence in data['intents']:
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

# vectorize data, limit the vocab, turning text into space-separated sequences
# of words, then split into list of tokens
# oov-value of of token
tokenizer=Tokenizer(num_words=1000,oov_token="<OOV>")
tokenizer.fit_on_texts(sample_sentences)
word_index=tokenizer.word_index
sequences=tokenizer.texts_to_sequences(sample_sentences)

# making all training text sequences into the same size
padded_sequences=pad_sequences(sequences, truncating='post', maxlen=20)

# neural network
model=Sequential()
model.add(Embedding(1000, 16, input_length=20))
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

# stochastic gradient descent (adam)
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# training the model
hist=model.fit(padded_sequences, np.array(sample_labels), epochs=500)

# save the model
model.save("bot_model")

# save the tokenizer and encoder
import pickle
with open('tokenizer.pickle', 'wb') as token:
    pickle.dump(tokenizer, token, protocol=pickle.HIGHEST_PROTOCOL)
with open('label_encoder.pickle', 'wb') as enc:
    pickle.dump(label_encoder, enc, protocol=pickle.HIGHEST_PROTOCOL)