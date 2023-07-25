from classification_training.training import start_training
from classification_training.chatbot import chatbot
from classification_training.database import User
from colors import prsys, insys
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)


def classification(username_in, loop_n, mode):
    username=User(username_in)
    name,flag=username.name()
    if loop_n==0:
        if username.username.lower()!='user':
            if flag==False:
                yn = insys("Do you want changes [y/n]: ")
                while yn.lower()=='y':
                    changes = insys("Change name: 'c', \nDelete user: 'd', \n's' to skip: ")
                    if changes.lower()=='c':
                        name=username.change_name()
                    elif changes.lower()=='d':
                        username_in=username.del_name()
                    elif changes.lower() not in ['c', 'd', 's']:
                        prsys("Invalid input")
                    else: 
                        break
                    yn = insys("Do you want more changes [y/n]: ")
                prsys(f"Logged as: {name}")
        
        return name
    epochs=username.userdata[username.username]
    elem_count_old = username.lessons_length()
    temp = elem_count_old
    # if mode==1:prsys(f"lessons length: {temp}")
    """train only if there are changes or its a new user"""
    if (temp != elem_count_old):
        epoch_upd=start_training(mode,username.path,epochs)
        """update number of epochs to speed up the training"""
        username.userdata[username.username]=epoch_upd
        dictoflabels=username.dict_update()
        username.userdb[username.username]=dictoflabels
    else:dictoflabels=username.userdb[username.username]
    inp=chatbot(name,username.path,mode)
    elem_count_new = username.lessons_length()
    temp=elem_count_new+1
    return inp
