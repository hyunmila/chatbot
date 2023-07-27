import transformers
import tensorflow as tf
import time
from colors import prsys, prbot
from functools import partial
from transformers import AutoTokenizer, TFAutoModelForCausalLM
from classification import classification
# from classification_training.database import Database
transformers.logging.set_verbosity_error()
from transformers_training.paths import path_pre, path_tun
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

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
model=TFAutoModelForCausalLM.from_pretrained(model_tun)

def exec_time(s,e):
    prsys(f"Took: {round((e-s),2)} s")

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

def main():
    mode=1
    train=0
    loop_n=0
    tf.random.set_seed(50)
    print("\nCHATBOT\n")
    username_in='user'
    name=classification(username_in,mode,train,loop_n)
    prbot(f"Hello {name}, start texting, type 'exit' to stop.")
    loop_n=1
    # algorithms={'0': "Greedy search",
    #             '1': "Beam search",
    #             '2': "Random sampling",
    #             '3': "Top-k sampling",
    #             '4': "Nucleus sampling"}
    while True:
        inp=classification(username_in,mode,train,loop_n)
        if inp.lower()=='exit':
            prsys("Quitting....")
            break
        s=time.time()
        generator = partial(generate, model=model, tokenizer=tokenizer)
        # prbot("\n0: Bot: ",generator(inp)[0])
        # prbot("1: Bot: ",generator(inp, num_beams=10, early_stopping=True, num_return_sequences=5,no_repeat_ngram_size=2)[0])
        prbot(f"{generator(inp, do_sample=True, top_k=0, temperature=0.8)[0]}")
        e=time.time()
        if mode==1:exec_time(s,e)
        # prbot("3: Bot: ",generator(inp, do_sample=True, top_k=50)[0])
        # prbot("4: Bot: ",generator(inp, do_sample=True, top_k=0, top_p=0.9)[0])

main()

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
