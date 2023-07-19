import transformers
import tensorflow as tf
from functools import partial
from transformers import pipeline, Conversation
from transformers import AutoTokenizer, TFAutoModelForCausalLM
transformers.logging.set_verbosity_error()
from paths import path_pre, path_tun

# model used here: DialoGPT-medium
# clone with git clone https://huggingface.co/microsoft/DialoGPT-medium
# if you have a problem with cloning the repo, use "git config http.sslVerify false" and "git config http.sslVerify true" after downloading
model_pre=path_pre() # path to a dir with pretrained model; ex: ".../VSC/transformers/DialoGPT-medium"

model_tun=path_tun() # path to a dir where fine-tuned model is saved; ex: ".../VSC/chatbot/transformers_bot/model"

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
        output_list.append(
            tokenizer.decode(
                output[input_ids.shape[-1]:], skip_special_tokens=True
            )
        )
    return output_list


print("\n\nCHATBOT LOADED\n\n")
while True:
    inp=input("User: ")
    if inp.lower()=='exit':break
    generator = partial(generate, model=model, tokenizer=tokenizer)
    print("Bot: ",generator(inp)[0])    

