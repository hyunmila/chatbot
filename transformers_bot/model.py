from statistics import mode
import statistics
import numpy as np
import transformers
import tensorflow as tf
from functools import partial
from transformers import pipeline, Conversation
from transformers import AutoTokenizer, TFAutoModelForCausalLM
transformers.logging.set_verbosity_error()
from paths import path_pre, path_tun

"""
model used here: DialoGPT-medium
clone with git clone https://huggingface.co/microsoft/DialoGPT-medium
if you have a problem with cloning the repo, use "git config http.sslVerify false" and "git config http.sslVerify true" after downloading
path to a dir with pretrained model; ex: '.../VSC/transformers/DialoGPT-medium'
"""
model_pre=path_pre() 
"""path to a dir where fine-tuned model is saved; ex: '.../VSC/chatbot/transformers_bot/model'"""
model_tun=path_tun() 

tokenizer=AutoTokenizer.from_pretrained(model_pre)
tokenizer.pad_token=tokenizer.eos_token
model=TFAutoModelForCausalLM.from_pretrained(model_tun)

def chat_pipeline(model_pre):
    bot = pipeline(task='conversational',
                        model=model_pre,
                        tokenizer=model_pre)
    inp=input("User: ")
    c1=Conversation(inp)
    while True:
        if inp.lower()=='exit':break
        c1=bot(c1)
        print("Bot: ",c1.generated_responses[-1])
        
        c1.mark_processed()
        inp=input("User: ")
        c1.add_user_input(inp)

# chat_pipeline(model_pre)

def generate(prompt, model, tokenizer, **kwargs):
    input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="tf")
    history_ids = model.generate(input_ids, max_length=1000,**kwargs)
    output_list = []
    for output in history_ids:
        """output[input_ids.shape[-1]:] is the exctracted list of tokenixed indexes of the response"""
        output_list.append(
            tokenizer.decode(
                output[input_ids.shape[-1]:], skip_special_tokens=True
            )
        )
    return output_list

tf.random.set_seed(50)
print("\n\nCHATBOT LOADED\n")
choices=[]
algorithms={'0': "Greedy search",
            '1': "Beam search",
            '2': "Random sampling",
            '3': "Top-k sampling",
            '4': "Nucleus sampling"}
while True:
    inp=input("\nUser: ")
    if inp.lower()=='exit':
        try:
            print("Best answers: ",algorithms[mode(choices)])
        except (statistics.StatisticsError, KeyError):
            break
        break
    generator = partial(generate, model=model, tokenizer=tokenizer)
    
    print("\n0: Bot: ",generator(inp)[0])
    print("1: Bot: ",generator(inp, num_beams=10, early_stopping=True, num_return_sequences=5,no_repeat_ngram_size=2)[0])
    print("2: Bot: ",generator(inp, do_sample=True, top_k=0, temperature=0.7)[0])
    print("3: Bot: ",generator(inp, do_sample=True, top_k=50)[0])
    print("4: Bot: ",generator(inp, do_sample=True, top_k=0, top_p=0.9)[0])
    choice=input("Which response fits your question best? [0,1,2,3,4]: ")
    choices.append(choice)

"""
A bit about the model.generate function:
    - greedy search (default one):
        Creates a list of tokens. It takes the encoded input
        and for each next word of response it creates a list
        of probabilities for each word in dictionary of the
        word that should be placed after the previous one. Then
        chooses index of the word with highest score and repeats 
        the process for next word in sentence. Then passes the
        list of tokenized indexes to the decoder. For the same
        sentence it will always give the same output (as the
        probabilities of the next word in the sentence after 
        the previos one were already calculated during training)
    - beam search:
        Calculates probability for the first word and probability for 
        every next word number of times specified in a given paramater,
        thus creating the same number of sentences (in this case 5).
        Then calculates the highest probability for every sentence
        and chooses the one with the highest score.
"""

