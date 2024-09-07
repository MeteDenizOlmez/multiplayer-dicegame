import socket
import _thread
import random
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 25565
ENCODING = "utf-8"
connections = []
addresses = []
connections_count = 0

# GameVariables
gameEnded = False


#Experimental Colours!
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



def mainGameEvent():
    def sendMsgToAll(msg):
        time.sleep(0.05)
        msg = f"[info] {msg}"
        time.sleep(0.05)
        player1_conn.sendall(msg.encode(ENCODING))
        time.sleep(0.05)
        player2_conn.sendall(msg.encode(ENCODING))
        time.sleep(0.05)


    print("main game start")
    #gameStarted = True
    #ASSIGN PLAYER 1 AND PLAYER 2
    #player1_addr = addresses[0]
    #player2_addr = addresses[1]
    player1_conn = connections[0]
    player2_conn = connections[1]

    print("connections count confirmed")
    
    sendMsgToAll("Waiting for Player 1 to enter their username...")
    
    msg = "[input] Player 1 Username: "
    print(player1_conn)
    player1_conn.sendall(msg.encode(ENCODING))

    response = player1_conn.recv(1024).decode()

    player1 = response
    player1_score = 0
    print(player1)

    sendMsgToAll(f"{player1} has joined the game!")

    print("stage 2 (new)")

    sendMsgToAll("Waiting for Player 2 to enter their username...")
    #check for player 2 username
    msg = "[input] Player 2 Username: "
    print(player2_conn)
    player2_conn.sendall(msg.encode(ENCODING))
    response = player2_conn.recv(1024).decode()
    player2 = response
    player2_score = 0
    print(player2)

    sendMsgToAll(f"{player2} has joined the game!")

    sendMsgToAll("Please standby for the game to start (You must start the game from the server console!)")
    input(f"{Style.WHITE}{Style.BG_YELLOW}Press ENTER to start the game...{Style.RESET}")

    # dice art dictionary
    dice_art = {
        1: ("┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘"),
        2: ("┌─────────┐",
            "│  ●      │",
            "│         │",
            "│      ●  │",
            "└─────────┘"),
        3: ("┌─────────┐",
            "│  ●      │",
            "│    ●    │",
            "│      ●  │",
            "└─────────┘"),
        4: ("┌─────────┐",
            "│  ●   ●  │",
            "│         │",
            "│  ●   ●  │",
            "└─────────┘"),
        5: ("┌─────────┐",
            "│  ●   ●  │",
            "│    ●    │",
            "│  ●   ●  │",
            "└─────────┘"),
        6: ("┌─────────┐",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "└─────────┘")
    }

    def diceRollArt(num):
        for i in range(5):
            sendMsgToAll(dice_art.get(num)[i]) #SEND MSG TO CLIENTS
            print(dice_art.get(num)[i])

    def diceRoll(player, player_score):
        roundScore = 0

        dice1 = random.randint(1, 6)
        diceRollArt(dice1)
        dice2 = random.randint(1, 6)
        diceRollArt(dice2)
        diceTotal = dice1 + dice2
        if diceTotal % 2 == 0:
            # even
            sendMsgToAll(f"[{player}] +10 POINTS --> Rolled an even!") #SEND MSG TO CLIENTS
            print(f"[{player}] +10 POINTS --> Rolled an even!")
            roundScore += 10
        else:
            # odd
            sendMsgToAll(f"[{player}] -5 POINTS --> Rolled an odd!") #SEND MSG TO CLIENTS
            print(f"[{player}] -5 POINTS --> Rolled an odd!")
            roundScore -= 5

        if dice1 == dice2:
            # roll extra dice
            sendMsgToAll(f"[{player}] EXTRA DICE ROLL --> Rolled a double!") #SEND MSG TO CLIENTS
            print(f"[{player}] EXTRA DICE ROLL --> Rolled a double!")

            if player == player1:
                msg = f"[input] [{player1}] Press ENTER to roll the dice..."
                #print("sending player1")
                player1_conn.sendall(msg.encode(ENCODING))
                #print("waiting to receive")
                response = player1_conn.recv(1024).decode()
                #print("received")
                
            elif player == player2:
                msg = f"[input] [{player2}] Press ENTER to roll the dice..."
                #print("sending player1")
                player2_conn.sendall(msg.encode(ENCODING))
                #print("waiting to receive")
                response = player2_conn.recv(1024).decode()
                #print("received")
            #input(f"[{player}] Press ENTER to roll the dice...")

            diceExtra = random.randint(1, 6)
            diceRollArt(diceExtra)

            sendMsgToAll(f"[{player}] +{diceExtra} POINTS --> Extra dice roll!") #SEND MSG TO CLIENTS
            print(f"[{player}] +{diceExtra} POINTS --> Extra dice roll!")
            roundScore += diceExtra

        sendMsgToAll(f"[{player}] +{diceTotal} POINTS --> Dice 1 + 2 Total") #SEND MSG TO CLIENTS
        print(f"[{player}] +{diceTotal} POINTS --> Dice 1 + 2 Total")
        roundScore += diceTotal

        # below 0? check
        if roundScore < 0:
            roundScore = 0

        player_score += roundScore

        return roundScore, player_score

    print("<game starting...>")


    roundNumber = 0
    while roundNumber < 5:
        roundNumber += 1
        sendMsgToAll("*************************") #SEND MSG TO CLIENTS
        sendMsgToAll(f"ROUND {roundNumber}") #SEND MSG TO CLIENTS
        sendMsgToAll("*************************") #SEND MSG TO CLIENTS

        print("*************************")
        print(f"ROUND {roundNumber}")
        print("*************************")

        # PLAYER 1
        msg = f"[input] [{player1}] Press ENTER to roll the dice..."
        print("sending player1")
        player1_conn.sendall(msg.encode(ENCODING))
        print("waiting to receive")
        response = player1_conn.recv(1024).decode()
        print("received")

        roundScore, player1_score = diceRoll(player1, player1_score)

        sendMsgToAll(f"[{player1}] ROUND SCORE = {roundScore}") #SEND MSG TO CLIENTS
        print(f"[{player1}] ROUND SCORE = {roundScore}")

        sendMsgToAll("*************************") #SEND MSG TO CLIENTS
        print("*************************")

        # PLAYER 2
        msg = f"[input] [{player2}] Press ENTER to roll the dice..."
        player2_conn.sendall(msg.encode(ENCODING))
        response = player2_conn.recv(1024).decode()

        roundScore, player2_score = diceRoll(player2, player2_score)
        
        sendMsgToAll(f"[{player2}] ROUND SCORE = {roundScore}") #SEND MSG TO CLIENTS
        sendMsgToAll("*************************") #SEND MSG TO CLIENTS
        
        print(f"[{player2}] ROUND SCORE = {roundScore}")
        print("*************************")

    sendMsgToAll("******************") #SEND MSG TO CLIENTS
    sendMsgToAll("TOTAL SCORES:") #SEND MSG TO CLIENTS
    sendMsgToAll("******************") #SEND MSG TO CLIENTS

    print("******************")
    print("TOTAL SCORES:")
    print("******************")

    sendMsgToAll(f"[{player1}] {player1_score} POINTS") #SEND MSG TO CLIENTS
    sendMsgToAll(f"[{player2}] {player2_score} POINTS") #SEND MSG TO CLIENTS

    print(f"[{player1}] {player1_score} POINTS")
    print(f"[{player2}] {player2_score} POINTS")

    if player1_score == player2_score:
        sendMsgToAll("******************") #SEND MSG TO CLIENTS
        sendMsgToAll("       TIE        ") #SEND MSG TO CLIENTS
        sendMsgToAll("******************") #SEND MSG TO CLIENTS

        print("******************")
        print("       TIE        ")
        print("******************")
        count = 0
        while nobodyWon:
            count += 1

            sendMsgToAll("*************************") #SEND MSG TO CLIENTS
            sendMsgToAll(f"EXTRA ROUND {count}") #SEND MSG TO CLIENTS
            sendMsgToAll("*************************") #SEND MSG TO CLIENTS

            print("*************************")
            print(f"EXTRA ROUND {count}")
            print("*************************")

            # PLAYER 1
            msg = f"[input] [{player1}] Press ENTER to roll the dice..."
            player1_conn.sendall(msg.encode(ENCODING))
            response = player1_conn.recv(1024).decode()

            roundScore, player1_score = diceRoll(player1, player1_score)

            sendMsgToAll(f"[{player1}] ROUND SCORE = {roundScore}") #SEND MSG TO CLIENTS

            print(f"[{player1}] ROUND SCORE = {roundScore}")

            sendMsgToAll("*************************") #SEND MSG TO CLIENTS
            print("*************************")

            # PLAYER 2
            msg = f"[input] [{player2}] Press ENTER to roll the dice..."
            player2_conn.sendall(msg.encode(ENCODING))
            response = player2_conn.recv(1024).decode()

            roundScore, player2_score = diceRoll(player2, player2_score)

            sendMsgToAll(f"[{player2}] ROUND SCORE = {roundScore}") #SEND MSG TO CLIENTS
            sendMsgToAll("*************************") #SEND MSG TO CLIENTS

            print(f"[{player2}] ROUND SCORE = {roundScore}")
            print("*************************")

            if player1_score > player2_score:
                sendMsgToAll(f"WINNER: {player1}") #SEND MSG TO CLIENTS
                print(f"WINNER: {player1}")
                nobodyWon = False
            elif player2_score > player1_score:
                sendMsgToAll(f"WINNER: {player2}") #SEND MSG TO CLIENTS
                print(f"WINNER: {player2}")
                nobodyWon = False
            else:
                pass




    elif player1_score > player2_score:
        sendMsgToAll(f"WINNER: {player1}") #SEND MSG TO CLIENTS
        print(f"WINNER: {player1}")
    else:
        sendMsgToAll(f"WINNER: {player2}") #SEND MSG TO CLIENTS
        print(f"WINNER: {player2}")
    
    #gameEnded = True
    print("GAME ENDED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    input("\nGame Ended!\nYou may now quit the SERVER and CLIENTS safely! \n (ENTER to test experimental replay mode...)\n")
    with player1_conn:
        connection.close()
    with player2_conn:
        connection.close()


def onConnection(clientConn, clientAddr, connections_count):
    while True:
        with clientConn:
            alive = True
            connections.append(clientConn)
            addresses.append(clientAddr)

            while alive:
                #print("checking")
                if connections_count == 2 and gameEnded == False:
                    print("main game can start")
                    # game has not yet started, and there are enough players to start:
                    mainGameEvent()
                elif connections_count == 2 and gameEnded == True:
                    print(f"{Style.WHITE}{Style.BG_RED}Game has ended!{Style.RESET}")
                    alive = False

                #try:

                    #clientConn.sendall(("[alivecheck]").encode(ENCODING))
                #except ConnectionError:
                    #print(f"{Style.WHITE}{Style.BG_RED}Client {clientAddr} has DISCONNECTED!{Style.RESET}")
                    #if clientConn in connections:
                        # print(">>>>>>>TEST IF CONNECTION IS ACTUALLY REMOVED HERE! <<<<<<")
                        # print("Connection should be removed from connections list")
                        # print("\n ACTIVE CONNECTIONS LIST CURRENTLY: ", connections)
                        #alive = False
                        #break

            connection.close()
            connections_count -= 1
            connections.remove(clientConn)
            address.remove(clientAddr)
            print(f"Current connections count: {connections_count}")
            # print("\n ACTIVE CONNECTIONS LIST CURRENTLY: ", connections)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Server Open on {SERVER_IP}:{SERVER_PORT}")

s.bind((SERVER_IP, SERVER_PORT))
print(f"Waiting for incoming connections (5)")
s.listen(5)

while True:
    # CONNECTION LIMIT REACHED
    if connections_count >= 2:
        connection, address = s.accept()
        print(
            f"{Style.WHITE}{Style.BG_YELLOW}Client {address} has attempted a connection, however, the limit for connections_count has been reached!{Style.RESET}")
        with connection:
            try:
                msg = f"Client {address} has attempted a connection, however, the limit for connections_count has been reached!"
                connection.send(msg.encode(ENCODING))
            except:
                pass
        try:
            connection.close()
            print("connection closed")
        except:
            pass
    else:
        connection, address = s.accept()
        connections_count += 1
        _thread.start_new_thread(onConnection, (connection, address, connections_count))
        print(f"{Style.WHITE}{Style.BG_GREEN}Client {address} has CONNECTED!{Style.RESET}")
        print("\n ACTIVE CONNECTIONS: ", connections)


