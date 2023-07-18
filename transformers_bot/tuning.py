import transformers
import tensorflow as tf
import numpy as np
import datasets
import math
import pandas as pd
from transformers import AutoTokenizer, TFAutoModelForCausalLM, AdamWeightDecay
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

transformers.logging.set_verbosity_error()

model_pre="C:/Users/kamilak/Documents/VSC/transformers/DialoGPT-medium"
tokenizer=AutoTokenizer.from_pretrained(model_pre)
tokenizer.pad_token=tokenizer.eos_token
model=TFAutoModelForCausalLM.from_pretrained(model_pre)

train=[
    {
        'label':0,
        'dialog':[
            "But what about second breakfast?",
            "Don't think he knows about second breakfast, Pip.",
            "What about elevensies?"]
    },
    {
        'label':1,
        'dialog':[
            "I didn't think it would end this way",
            "End? No, the journey doesn't end here.",
            "Well it isn't so bad"]
    }
]
validate=[
    {
        'label':0,
        'dialog':[
            "It's a Dangerous Business, Frodo, Going Out Your Door.",
            "Remember what Bilbo used to say",
            "There's no knowing where they might be swept off to."
        ]
    },
    {
        'label':1,
        'dialog':[
            "I never thought I would die fighting side by side with an Elf.",
            "What about side by side with a friend?",
            "That will do."
        ]
    }
]

train=datasets.Dataset.from_pandas(pd.DataFrame(data=train))
validate=datasets.Dataset.from_pandas(pd.DataFrame(data=validate))
dataset=datasets.DatasetDict({'train': train, 'validate':validate})

def concatenate_utterances(example):
    example['dialog'] = " ".join(example['dialog'])
    return example

dataset=dataset.map(concatenate_utterances)

def encode(examples):
    encoded = tokenizer(examples['dialog'], truncation=True, padding=True, max_length=26)
    encoded['labels'] = encoded['input_ids'][:]
    return encoded

encoded_dataset = dataset.map(encode, batched=True, remove_columns=['dialog'])

optimizer=AdamWeightDecay(learning_rate=2e-5, weight_decay_rate=0.01)
model.compile(optimizer=optimizer)

tv=np.array(encoded_dataset['train']['labels'])
lv=np.array(encoded_dataset['validate']['labels'])
labels=np.array(tf.cast(tv, dtype=tf.int32))
eval_labels=np.array(tf.cast(lv, dtype=tf.int32))
tf_train_dataset=pad_sequences(encoded_dataset['train']['input_ids'], truncating='post', maxlen=26)
eval_dataset=pad_sequences(encoded_dataset['validate']['input_ids'], truncating='post', maxlen=26)
tf_eval_dataset=(eval_dataset, eval_labels)

model.fit(tf_train_dataset, labels, validation_data=tf_eval_dataset, epochs=10)
model.save_pretrained("C:/Users/kamilak/Documents/VSC/chatbot/transformers_bot/model")
eval_loss = model.evaluate(eval_dataset, eval_labels)

print(f"Perplexity: {math.exp(eval_loss):.2f}")

model=TFAutoModelForCausalLM.from_pretrained("C:/Users/kamilak/Documents/VSC/chatbot/transformers_bot/model")

test_sentence="But what about second breakfast?"
tokenized = tokenizer(test_sentence, return_tensors="np")

outputs = model.generate(**tokenized, max_length=26)

print(outputs)
print(tokenizer.decode(outputs[0]))