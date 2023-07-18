import transformers
from transformers import pipeline, Conversation
from tuning import tuning
transformers.logging.set_verbosity_error()

model_pre="C:/Users/kamilak/Documents/VSC/transformers/DialoGPT-medium"

bot = pipeline(task='conversational',
                    model=model_pre,
                    tokenizer=model_pre)
def main():
    bot=tuning()
    inp=input("User: ")
    c1=Conversation(inp)
    while True:
        if inp.lower()=='exit':break
        
        c1=bot(c1)
        print("Bot: ",c1.generated_responses[-1])
        inp=input("User: ")
        c1.add_user_input(inp)

main()