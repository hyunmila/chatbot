import time
import shelve
import numpy as np
from bot_module.training import training
from bot_module.chatbot import chatbot, lessons_length


def main():
    userdata = shelve.open("userdata/userdata")
    mode = 0 # 1 for debug, 0 for user
    username = input("Enter your username or 's' to skip: ")
    if (username not in list(userdata.keys())):
        name=input("Enter your name or 's' to skip: ")
        if name.lower()=='s':
            name="User"+str(np.random.randint(100))
            print("Name: ", name)
        userdata[username]=name
    name=userdata[username]
    if username.lower()!='s':
        yn = input("Do you want changes [y/n]: ")
        while yn.lower()=='y':
            changes = input("Change name: 'c', \nDelete user: 'd', \n's' to skip: ")
            if changes.lower()=='c':
                userdata[username]=input("Name: ")
                name=userdata[username]
            elif changes.lower()=='d':
                todel = input("Username: ")
                if (todel.lower()=='s' or todel==username):
                    print("Can't delete that one!")
                else:
                    del userdata[todel]
            yn = input("Saved! Do you want more changes [y/n]: ")
        print("Logged as: ", username, ": ", name)
    i=0
    elem_count_old = lessons_length()
    temp = elem_count_old
    
    while True:
        if i%2==0:
            if temp != elem_count_old: # train only if there are changes
                training(mode)
            time.sleep(1)
            print("Main loaded")
            i+=1
        if i%2!=0:
            chatbot(name)
            elem_count_new = lessons_length()
            temp=elem_count_new
            i+=1

main()