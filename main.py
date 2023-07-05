import time
import shelve
import shutil
import os
import warnings
import numpy as np
from bot_module.training import start_training
from bot_module.chatbot import chatbot, lessons_length
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

def main():
    # 1 for debug, 0 for user
    mode = 0

    is_new=False # new user training
    usernames=shelve.open("bot_module/database/userdata/usernames")
    userdata=shelve.open("bot_module/database/userdata/userdata")
    userdb=shelve.open("bot_module/database/userdata/userdb")
    # check if database is full, if not delete additional entries
    db_list=os.listdir(path='bot_module/database')
    db_list.remove('userdata')
    lengths=[len(list(usernames.keys())), len(list(userdata.keys())), len(db_list), len(list(userdb.keys()))]
    is_not_equal = (lengths[0]!=lengths[1] or lengths[0]!=lengths[2] or lengths[0]!=lengths[3]) # True if not equal
    while is_not_equal:
        yn=input("Database error, continue? [y/n]: ")
        if yn.lower()=='n':break
        count=lengths.count(max(lengths))
        id=lengths.index(max(lengths))
        match id:
            case 0:
                for elem in list(usernames.keys()):
                    if (elem not in list(userdata.keys())) or (elem not in db_list) or (elem not in list(userdb.keys())):
                        print("Deleting ",elem," from usernames")
                        del usernames[elem]
                        lengths[0]=len(list(usernames.keys()))
            case 1:
                for elem in list(userdata.keys()):
                    if (elem not in list(usernames.keys())) or (elem not in db_list) or (elem not in list(userdb.keys())):
                        print("Deleting ",elem," from userdata")
                        del userdata[elem]
                        lengths[1]=len(list(userdata.keys()))
            case 2:
                for elem in db_list:
                    if (elem not in list(userdata.keys())) or (elem not in list(usernames.keys())) or (elem not in list(userdb.keys())):
                        print("Deleting ",elem," from database")
                        try:
                            shutil.rmtree('bot_module/database/'+str(elem))
                        except NotADirectoryError:
                            os.remove('bot_module/database/'+str(elem))
                        db_list=os.listdir(path='bot_module/database')
                        db_list.remove('userdata')
                        lengths[2]=len(db_list)
            case 3:
                for elem in list(userdb.keys()):
                    if (elem not in list(userdata.keys())) or (elem not in list(usernames.keys())) or (elem not in db_list):
                        print("Deleting ",elem," from userdb")
                        del userdb[elem]
                        lengths[3]=len(list(userdb.keys()))
        count=lengths.count(max(lengths))
        if count==3:
            is_not_equal=False
        
    username = input("Enter your username or 's' to skip: ")
    if username.lower()=='s':
            username='user'
    if (username not in list(usernames.keys())):
        is_new=True
        # add user to the database
        name=input("Enter your name or 's' to skip: ") 
        if name.lower()=='s':
            name="User"+str(np.random.randint(100)) # hardcoded num
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
                    del userdb[todel]
                    shutil.rmtree('bot_module/database/'+str(todel))
                    username='user'
                    name=usernames[username]
                    break
                else:
                    del usernames[todel]
                    del userdata[todel]
                    del userdb[todel]
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
    if mode==1:print("lessons length: ",temp)
    

    while True:
        if i%2==0:
            if (temp != elem_count_old or is_new): # train only if there are changes or its a new user
                epoch_upd, dictoflabels=start_training(mode,path,num_epochs)
                userdata[username]=epoch_upd # update number of epochs to speed up the training
                userdb[username]=dictoflabels
            else:dictoflabels=userdb[username]
            time.sleep(1)
            print("Main loaded")
            i+=1
        if i%2!=0:
            chatbot(name,path,mode,dictoflabels,username)
            elem_count_new = lessons_length(path)
            temp=elem_count_new+1
            if mode==1:print(temp)
            i+=1

main()