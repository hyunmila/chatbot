# chatbot
This chatbot uses two modules: the first one is responsible for classifying the question and selecting response from given database it was taught, if the question is new, bot will come up with an answer created of words from the dictionary it was pre-trained and later fine-tuned on. 
## classification_training
Chatbot model trained using neural networks.
The training model structure is an extended version of code found here: https://github.com/amilavm/Chatbot_Keras.

## transformers_training
Chatbot model fine-tuned DialoGPT with my own dataset of conversations using Huggingface Transformers library and Keras Tensorflow.