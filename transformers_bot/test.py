import transformers
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf
import numpy as np

transformers.logging.set_verbosity_error()
checkpoint="C:/Users/kamilak/Documents/VSC/transformers/distilbert-base-uncased-finetuned-sst-2-english"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
raw_inputs = [
    "I hate this so much!",
    "I love you!",
    "I don't like apples."
]

inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="tf")
# print(inputs)

model = TFAutoModelForSequenceClassification.from_pretrained(checkpoint)
outputs = model(inputs)
predictions = tf.math.softmax(outputs.logits, axis=-1)
label=model.config.id2label
# print(label)
# print(predictions)
lista=predictions.numpy()

for i in range(len(raw_inputs)):
    id=np.where(lista[i]==max(lista[i]))
    print(f"Message -{raw_inputs[i]}- is {label[id[0][0]]}")


