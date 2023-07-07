import shelve
import time
import numpy as np
import shutil
import json
from bot_module.chatbot import chatbot

from bot_module.training import start_training

class User:
    def __init__(self, username):
        self.username=username
        self.path='bot_module/database/'+str(self.username)
        self.usernames=shelve.open("bot_module/database/userdata/usernames")
        self.userdata=shelve.open("bot_module/database/userdata/userdata")
        self.userdb=shelve.open("bot_module/database/userdata/userdb")
        self.epochs=self.userdata[self.username]
    
    def database(self):
        with open(str(self.path)+'/lessons.json') as lessons:
            self.data = json.load(lessons)
            return self.data
    
    def is_new(self):
        if (self.username not in list(self.usernames.keys())):
            return True

    def name(self):
        if self.is_new():
            self.name=input("Enter your name or 's' to skip: ")
            if self.name.lower()=='s':
                self.name="User"+str(np.random.randint(100)) # hardcoded num
                print("Name: ", self.name)
            self.usernames[self.username]=self.name
            source_dir='bot_module/database/user' 
            destination_dir=self.path
            shutil.copytree(source_dir,destination_dir)
            self.userdata[self.username]=100
            dictoflabels=self.dict_update()
            self.userdb[self.username]=dictoflabels
        else:
            self.name=self.usernames[self.username]
        return self.name

    def dict_update(self):
        data=self.database()
        dictoflabels={}
        for i in range(len(data['lessons'])):
            key=((data['lessons'])[i]['tag'])
            dictoflabels[key]=i
        return dictoflabels

    def change_name(self):
        self.usernames[self.username]=input("Name: ")
        return self.usernames[self.username]

    def delete_from(self,todel):
        for elem in ([self.usernames, self.userdata, self.userdb]):
            print(list(elem))
            print("Deleting: ", elem[todel])
            del elem[todel]
            print(list(elem))
        shutil.rmtree('bot_module/database/'+str(todel))

    def del_name(self):
        todel = input("Username: ")
        if (todel.lower()=='user' or todel not in list(self.usernames.keys())):
            print("Can't delete that one!")
        elif todel==self.username:
            print(todel)
            self.delete_from(todel)
            return 'user'
        else:
            self.delete_from(todel)
    
    def lessons_length(self):
        data=self.database('lessons')
        elem_count=0
        for elem in data['lessons']:
            elem_count+=1
        return elem_count
    




def main():
    # 1 for debug, 0 for user
    mode = 0


    username_in = input("Enter your username or 's' to skip: ")
    if username_in.lower()=='s':
        username_in='user'
    username=User(username_in)
    print(username.username, username.path)
    name=username.name()
    if username_in.lower()!='user' or not username.is_new():
        yn = input("Do you want changes [y/n]: ")
        while yn.lower()=='y':
            changes = input("Change name: 'c', \nDelete user: 'd', \n's' to skip: ")
            if changes.lower()=='c':
                name=username.change_name()
            elif changes.lower()=='d':
                username_in=username.del_name()
                username=User(username_in)
                name=username.name()
                print(username.username,name)
                break
            elif changes.lower() not in ['c', 'd', 's']:
                print("Invalid input")
            else: 
                break
            yn = input("Do you want more changes [y/n]: ")
        print("Logged as: ", name)
    i=0
    elem_count_old = username.lessons_length()
    temp = elem_count_old
    if mode==1:print("lessons length: ",temp)
    

    while True:
        if i%2==0:
            if (temp != elem_count_old): # train only if there are changes or its a new user
                epoch_upd=start_training(mode,username.path,username.epochs)
                username.userdata[username]=epoch_upd # update number of epochs to speed up the training
                dictoflabels=username.dict_update()
                username.userdb[username]=dictoflabels
            else:dictoflabels=username.userdb[username]
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