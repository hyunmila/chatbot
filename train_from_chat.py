import json
from training import training



def learning_from_chat():
    with open('lessons.json') as read:
        dataread = json.load(read)


    elem_count=0
    for elem in dataread['lessons']:
        elem_count+=1

    i=0
    j=1
    while True:

        if i%2==0:
            print("User: ", end="")
            inp1 = input()
            if inp1.lower()=="exit":
                break
            i=i+1
        if i%2!=0:
            print("User: ", end="")
            inp2 = input()
            if inp2.lower()=="exit":
                break
            i=i+1
        
        
        data = {"tag":"lesson"+str(elem_count+j),"questions":[inp1],"responses":[inp2]}
        j=j+1
        with open('lessons.json','r+') as file:
            filedata=json.load(file)
            filedata["lessons"].append(data)
            file.seek(0)
            json.dump(filedata, file)
    
# learning_from_chat()

