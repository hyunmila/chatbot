import os
import shelve
import numpy as np
import shutil
import json

class User:
    def __init__(self, username):
        self.username=username
        self.path='bot_module/database/'+str(self.username)
        self.usernames=shelve.open("bot_module/database/userdata/usernames")
        self.userdata=shelve.open("bot_module/database/userdata/userdata")
        self.userdb=shelve.open("bot_module/database/userdata/userdb")
    
    def database(self):
        with open(str(self.path)+'/lessons.json') as lessons:
            self.data = json.load(lessons)
            return self.data
    
    def is_new(self):
        if (self.username not in list(self.usernames.keys())):
            return True
        else:
            return False

    def name(self):
        flag=False
        if self.is_new():
            flag=True
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
        return self.name,flag

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
            # print("Deleting: ", elem[todel])
            del elem[todel]
        shutil.rmtree('bot_module/database/'+str(todel))

    def del_name(self):
        todel = input("Username: ")
        if (todel.lower()=='user' or todel not in list(self.usernames.keys())):
            print("Can't delete that one!")
        elif todel==self.username:
            self.delete_from(todel)
            return 'user'
        else:
            self.delete_from(todel)
            return self.username
    
    def lessons_length(self):
        data=self.database()
        elem_count=0
        for elem in data['lessons']:
            elem_count+=1
        return elem_count
    


class Database:
    def __init__(self):
        self.usernames=shelve.open("bot_module/database/userdata/usernames")
        self.userdata=shelve.open("bot_module/database/userdata/userdata")
        self.userdb=shelve.open("bot_module/database/userdata/userdb")
        self.db_list=os.listdir(path='bot_module/database')
        self.db_list.remove('userdata')
        self.keys_list=[list(self.usernames.keys()), list(self.userdata.keys()),
                        list(self.userdb.keys()), self.db_list]
    
    def list_len(self):
        lengths=[len(self.keys_list[0]), len(self.keys_list[1]), 
                    len(self.keys_list[2]), len(self.keys_list[3])]
        return lengths
    
    def del_from_list(self,id,lengths):
        if id==3:
            for elem in self.keys_list[id]:
                if ((elem not in self.keys_list[0]) or
                    (elem not in self.keys_list[1]) or
                    (elem not in self.keys_list[2])):
                    print("Deleting ",elem," from database")
                    try:
                        shutil.rmtree('bot_module/database/'+str(elem))
                    except NotADirectoryError:
                        os.remove('bot_module/database/'+str(elem))
                    self.db_list.remove(elem)
                    lengths[id]=len(self.db_list)
        else:
            list_todel=self.keys_list[id]
            temp=self.keys_list.copy()
            temp.pop(id)
            userx_list=[self.usernames,self.userdata,self.userdb]
            for elem in list_todel:
                if ((elem not in temp[0]) or
                    (elem not in temp[1]) or
                    (elem not in temp[2])):
                    print("Deleting ",elem,":",userx_list[id][elem])
                    del (userx_list[id][elem])
                    lengths[id]=len(list((userx_list[id]).keys()))
        return lengths

    def is_equal(self):
        lengths=self.list_len()
        is_not=(lengths[0]!=lengths[1] or lengths[0]!=lengths[2] or lengths[0]!=lengths[3]) # True if not equal
        while is_not:
            yn=input("Database error, continue? [y/n]: ")
            if yn.lower()=='n':break
            count=lengths.count(max(lengths))
            id=lengths.index(max(lengths))
            lengths=self.del_from_list(id,lengths)
            count=lengths.count(max(lengths))
            if count==4:
                is_not=False

