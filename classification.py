import time
from classification_training.training import start_training
from classification_training.chatbot import chatbot
from classification_training.database import User, Database

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)


def main():
    # 1 for debug, 0 for user
    mode = 0

    Database().is_equal()
    username_in = input("Enter your username or 's' to skip: ")
    if username_in.lower()=='s':
        username_in='user'
    username=User(username_in)
    name,flag=username.name()
    if username.username.lower()!='user':
        if flag==False:
            yn = input("Do you want changes [y/n]: ")
            while yn.lower()=='y':
                changes = input("Change name: 'c', \nDelete user: 'd', \n's' to skip: ")
                if changes.lower()=='c':
                    name=username.change_name()
                elif changes.lower()=='d':
                    username_in=username.del_name()
                elif changes.lower() not in ['c', 'd', 's']:
                    print("Invalid input")
                else: 
                    break
                yn = input("Do you want more changes [y/n]: ")
            print("Logged as: ", name)
    i=0
    epochs=username.userdata[username.username]
    elem_count_old = username.lessons_length()
    temp = elem_count_old
    if mode==1:print("lessons length: ",temp)
    
    while True:
        if i%2==0:
            if (temp != elem_count_old): # train only if there are changes or its a new user
                epoch_upd=start_training(mode,username.path,epochs)
                username.userdata[username.username]=epoch_upd # update number of epochs to speed up the training
                dictoflabels=username.dict_update()
                username.userdb[username.username]=dictoflabels
            else:dictoflabels=username.userdb[username.username]
            time.sleep(1)
            print("Main loaded")
            i+=1
        if i%2!=0:
            chatbot(name,username.path,mode,dictoflabels,username.username)
            elem_count_new = username.lessons_length()
            temp=elem_count_new+1
            if mode==1:print(temp)
            i+=1

main()