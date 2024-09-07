import socket
class Style():
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    RESET = "\033[0m"


def experimentalOption():
    choice = input("Would you like to enable the EXPERIMENTAL colour setting? (Y/N)")
    if choice == "N":
        Style.RED = ""
        Style.GREEN = ""
        Style.YELLOW = ""
        Style.BLUE = ""
        Style.MAGENTA = ""
        Style.CYAN = ""
        Style.WHITE = ""

        Style.BG_BLACK = ""
        Style.BG_RED = ""
        Style.BG_GREEN = ""
        Style.BG_YELLOW = ""
        Style.BG_BLUE = ""
        Style.BG_MAGENTA = ""
        Style.BG_CYAN = ""
        Style.BG_WHITE = ""

        Style.RESET = ""
    elif choice == "Y":
        pass
    else:
        print("Please enter an appropriate response (Y/N) !")
        experimentalOption()
        

experimentalOption()


print(f"{Style.WHITE}{Style.BG_CYAN}Multiplayer Connection System: {Style.RESET}")
while True:
    try:
        HOST = str(input("HOST: "))
        PORT = int(input("PORT: "))
    except:
        print(f"{Style.WHITE}{Style.BG_RED}Please ensure you have entered the correct values! (HOST should be a string, PORT should be an integer){Style.RESET}")
    else:
        break

#HOST = "127.0.0.1"
#PORT = 25565
ENCODING = 'utf-8'
print(f"Connecting to {HOST}:{PORT}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#s.sendall(b"")

while True:
    data = s.recv(4096)
    #print("data received!")
    if "[input]" in (data.decode(ENCODING)):
        inputInfo = (data.decode(ENCODING)).strip("[input]")
        msg = input(f"{Style.WHITE}{Style.BG_YELLOW}{inputInfo}{Style.RESET}")
        
        if msg == "": #if its empty, make sure to send a space character so something is received on the server end
            msg = " "

        s.sendall(msg.encode())
        #print(msg.encode(ENCODING), "sent")
        #s.close()
        #data = s.recv(4096)
    elif "[alivecheck]" in (data.decode(ENCODING)):
        print("still alive!") # debug only!
    elif "[info]" in (data.decode(ENCODING)):
        print((data.decode(ENCODING)).strip("[info]"))


    #print(data.decode(ENCODING))

#input()
