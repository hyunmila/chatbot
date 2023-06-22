import json

# {"lessons":[
    
# ]}

i=0
while True:
    print("User: ", end="")
    if i%2==0:
        inp1 = input()
        # if inp1.lower()=="exit":
        #     break
        i=i+1
    if i%2!=0:
        inp2 = input()
        # if inp2.lower()=="exit":
        #     break
        i=i+1
    data = {"learning":[{"tag":"lesson"+str(i),"questions":inp1,"responses":inp2}]}
    # print(inp1, inp2, data)
    with open('log.json','r+') as file:
        filedata=json.load(file)
        filedata["lessons"].append(data)
        file.seek(0)
        json.dump(filedata, file)
    

