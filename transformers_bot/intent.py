import transformers
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf
import numpy as np
from paths import path_intent
transformers.logging.set_verbosity_error()

# model used here: distilbert-base-uncased-finetuned-sst-2-english
# clone with git clone https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english
# if you have a problem with cloning the repo, use "git config http.sslVerify false" and "git config http.sslVerify true" after downloading
checkpoint=path_intent() # path to a dir with pretrained model; ex: ".../VSC/transformers/distilbert-base-uncased-finetuned-sst-2-english"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
raw_inputs = [
    "I hate this so much!",
    "I love you!",
    "I don't like apples."
]

inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="tf")

model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint)
outputs = model(inputs)
predictions = tf.math.softmax(outputs.logits, axis=-1)
label=model.config.id2label
lista=predictions.numpy()

for i in range(len(raw_inputs)):
    id=np.where(lista[i]==max(lista[i]))
    print(f"Message -{raw_inputs[i]}- is {label[id[0][0]]}")

