
from training import training
from chat_bot import chatbot


name = "User"
i=0
while True:
    if i%2==0:
        print("Main loaded")
        training()
        i+=1
    if i%2!=0:
        chatbot(name)
        i+=1
