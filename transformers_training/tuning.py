import transformers
import tensorflow as tf
import numpy as np
import datasets
import math
import json
import pandas as pd
from transformers import AutoTokenizer, TFAutoModelForCausalLM, AdamWeightDecay
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from transformers_training.paths import path_pre, path_tun
transformers.logging.set_verbosity_error()
from colors import prsys

"""
model used here: DialoGPT-medium
clone with git clone https://huggingface.co/microsoft/DialoGPT-medium
if you have a problem with cloning the repo, use "git config http.sslVerify false" and "git config http.sslVerify true" after downloading
path to a dir with pretrained model; ex: '.../VSC/transformers/DialoGPT-medium'
"""
model_pre=path_pre() 
"""path to a dir where fine-tuned model is saved; ex: '.../VSC/chatbot/transformers_training/model'"""
model_tun=path_tun() 

tokenizer=AutoTokenizer.from_pretrained(model_pre)
tokenizer.pad_token=tokenizer.eos_token
model=TFAutoModelForCausalLM.from_pretrained(model_pre)

with open('transformers_training/data.json') as file:
    data=json.load(file)

train=data['data'][0]['train']
validate=data['data'][1]['validate']

train=datasets.Dataset.from_pandas(pd.DataFrame(data=train))
validate=datasets.Dataset.from_pandas(pd.DataFrame(data=validate))
dataset=datasets.DatasetDict({'train': train, 'validate':validate})

def concatenate_utterances(example):
    example['dialog'] = " ".join(example['dialog'])
    return example

dataset=dataset.map(concatenate_utterances)

def encode(examples):
    if i==0:
        encoded = tokenizer(examples['dialog'], truncation=True, padding=True)
    elif i==1:
        encoded = tokenizer(examples['dialog'], truncation=True, padding='max_length', max_length=max_len)
    encoded['labels'] = encoded['input_ids'][:]
    return encoded

def id_len(examples):
    max_len.append(len(examples['input_ids']))

max_len=40 
i=0
while True:
    check_len=max_len
    encoded_dataset = dataset.map(encode, batched=True, remove_columns=['dialog'])
    max_len=[]
    encoded_dataset.map(id_len)
    max_len=min(max_len)
    if check_len==max_len:break
    i+=1


optimizer=AdamWeightDecay(learning_rate=2e-5, weight_decay_rate=0.01)
model.compile(optimizer=optimizer)

tv=np.array(encoded_dataset['train']['labels'])
lv=np.array(encoded_dataset['validate']['labels'])
labels=np.array(tf.cast(tv, dtype=tf.int32))
eval_labels=np.array(tf.cast(lv, dtype=tf.int32))
tf_train_dataset=pad_sequences(encoded_dataset['train']['input_ids'], truncating='post', maxlen=max_len)
eval_dataset=pad_sequences(encoded_dataset['validate']['input_ids'], truncating='post', maxlen=max_len)
tf_eval_dataset=(eval_dataset, eval_labels)
# TODO:
"""This is potentially not the best idea as arrays will need to be fully loaded into memory
and it slows down training. Research on prepare_tf_dataset."""
model.fit(tf_train_dataset, labels, validation_data=tf_eval_dataset, epochs=10)
# model.summary()
model.save_pretrained(model_tun)
eval_loss = model.evaluate(eval_dataset, eval_labels)

prsys(f"Perplexity: {math.exp(eval_loss):.2f}")
