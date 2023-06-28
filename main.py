import time
from bot_module.training import training
from bot_module.chatbot import chatbot


def main():
    mode = 1 # 1 for debug, 0 for user
    name=input("Enter your name or skip: ")
    # name="User"
    if name=='skip':
        name="User"
    i=0
    while True:
        if i%2==0:
            time.sleep(1)
            print("Main loaded")
            training(mode)
            i+=1
        if i%2!=0:
            chatbot(name)
            i+=1

main()