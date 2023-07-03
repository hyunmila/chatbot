import time
import shelve
import shutil
import numpy as np
from bot_module.training import start_training
from bot_module.chatbot import chatbot, lessons_length


def main():
    mode = 0 # 1 for debug, 0 for user

    usernames=shelve.open("bot_module/database/userdata/usernames")
    userdata=shelve.open("bot_module/database/userdata/userdata")
    # TODO: check lists length, if unequal raise error
    username = input("Enter your username or 's' to skip: ")
    if username.lower()=='s':
            username='user'
    if (username not in list(usernames.keys())):
        # add user to the database
        name=input("Enter your name or 's' to skip: ") 
        if name.lower()=='s':
            name="User"+str(np.random.randint(100))
            print("Name: ", name)
        usernames[username]=name 
        # add user data to the database and create a model
        source_dir='bot_module/database/user' 
        destination_dir='bot_module/database/'+str(username)
        shutil.copytree(source_dir,destination_dir)
        userdata[username]=100
    else:
        name=usernames[username] 


    if username.lower()!='user':
        yn = input("Do you want changes [y/n]: ")
        while yn.lower()=='y':
            changes = input("Change name: 'c', \nDelete user: 'd', \n's' to skip: ")
            if changes.lower()=='c':
                usernames[username]=input("Name: ")
                name=usernames[username]
            elif changes.lower()=='d':
                todel = input("Username: ")
                if (todel.lower()=='user' or todel not in list(usernames.keys())):
                    print("Can't delete that one!")
                elif todel==username:
                    del usernames[todel]
                    del userdata[todel]
                    shutil.rmtree('bot_module/database/'+str(todel))
                    username='user'
                    name=usernames[username]
                    break
                else:
                    del usernames[todel]
                    del userdata[todel]
                    shutil.rmtree('bot_module/database/'+str(todel))
            elif changes.lower() not in ['c', 'd', 's']:
                print("Invalid input")
            else: 
                break
            yn = input("Do you want more changes [y/n]: ")
        print("Logged as: ", name)
        usernames.close()

    path='bot_module/database/'+str(username)
    num_epochs=userdata[username]
    i=0
    elem_count_old = lessons_length(path)
    temp = elem_count_old
    
    while True:
        if i%2==0:
            if temp != elem_count_old: # train only if there are changes
                epoch_upd=start_training(mode,path,num_epochs)
                userdata[username]=epoch_upd # update number of epochs to speed up the training
            time.sleep(1)
            print("Main loaded")
            i+=1
        if i%2!=0:
            chatbot(name,path)
            elem_count_new = lessons_length(path)
            temp=elem_count_new
            i+=1


main()