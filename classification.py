from classification_training.training import start_training
from classification_training.chatbot import chatbot
import shelve
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)


def classification(username_in, mode, train, loop_n):
    userdata=shelve.open("classification_training/database/userdata/userdata")
    name=userdata[username_in][0]
    epochs=userdata[username_in][1]
    path='classification_training/database/'+str(username_in)
    if loop_n==0:
        return name
    if train==1:
        epoch_upd=start_training(mode,path,epochs)
        """update number of epochs to speed up the training"""
        userdata[username_in][1]=epoch_upd
    inp=chatbot(name,path,mode)
    return inp

# classification('user',1,0)