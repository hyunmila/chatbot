def prsys(skk): 
    print("\033[93m{}\033[00m" .format("SYSTEM: "+skk))

def prbot(skk): 
    print("\033[92m{}\033[00m" .format("Bot: "), end="")
    print(skk)

def insys(skk):
    inp=input("\033[93m{}\033[00m" .format("System: "+skk))
    return inp
