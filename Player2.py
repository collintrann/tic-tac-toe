"""Host player. symbol o/O

Asks user for host address and port number to set up server. Waits for client to connect
and send username. Sends server username "player2" and waits for client to make first move.
Alternate moves until game is over, then waits for client response to either play another
or stop playing. If client wants to stop playing, print host game statistics.


"""

import socket
from BoardClass import BoardClass

def hostGamePlay(clientUsername: str, serverUsername: str, clientConnection: socket.socket):
    """Hosts game play until client wants to stop.
    
    Args:
    clientUsername: Client player's username.
    serverUsername: Host server's username.
    clientConnection: Client's socket connection."""
    #Start Game
    gameInstance = BoardClass(serverUsername, clientUsername)

    gameInstance.printInstructions()
    player1Symbol = "X"
    player2Symbol = "O"
    keepPlaying = True
    while (keepPlaying):
        #Get first move from client
        print("Waiting for " + clientUsername + "'s move...")
        clientMoveData = clientConnection.recv(1024)
        clientMove = clientMoveData.decode()
        gameInstance.updateBoard(int(clientMove), player1Symbol)
        print(clientUsername + " has made a move:")
        gameInstance.printBoard()
        #Update last person to make a move
        gameInstance.updateLastTurn(clientUsername)

        #Check if game is over and then ask if player wants to keep playing
        #Update game stats
        if gameInstance.gameOver():
            gameInstance.updateGamesPlayed()
            if gameInstance.isWinner():
                print("You lose.")
                gameInstance.updateLosses()
            elif gameInstance.boardIsFull():
                print("You and " + clientUsername + " tied.")
                gameInstance.updateTies()
            #Wait for client to respond if they want to keep playing
            print("Asking if " + clientUsername + " wants to keep playing...")
            keepPlayingData = clientConnection.recv(1024)
            keepPlaying = keepPlayingData.decode()
            if keepPlaying == "y":
                print("Board Reset.")
                gameInstance.resetGameBoard()
                continue
            elif keepPlaying == "n":
                gameInstance.resetGameBoard()
                print("Disconnecting...")
                break

        #Get move input from host
        print("Your turn. Your marker is: " + player2Symbol)
        playerMove = gameInstance.getInput()
        clientConnection.send(playerMove.encode())
        
        # Update Board with host move and send to client
        gameInstance.updateBoard(int(playerMove), player2Symbol)
        print("Your move:")
        gameInstance.printBoard()
        #Update last person to make a move
        gameInstance.updateLastTurn(serverUsername)

        #Check if game is over and then ask if player wants to keep playing
        #Update game stats
        if gameInstance.gameOver():
            gameInstance.updateGamesPlayed()
            if gameInstance.isWinner():
                print("You win!")
                gameInstance.updateWins()
            elif gameInstance.boardIsFull():
                print("You and " + clientUsername + " tied.")
                gameInstance.updateTies()
            #Wait for client to respond if they want to keep playing
            print("Asking if " + clientUsername + " wants to keep playing...")
            keepPlayingData = clientConnection.recv(1024)
            keepPlaying = keepPlayingData.decode()
            if keepPlaying == "y":
                print("Board Reset.")
                gameInstance.resetGameBoard()
                continue
            else:
                gameInstance.resetGameBoard()
                print("Disconnecting...")
                break
    gameInstance.printStats()
    print("Goodbye!")

def setUpGameServer():
    """Sets up server, waits for client to connect, and hosts gameplay.
    """
    hostAddress = input("Input host name or IP address to set up Tic-Tac-Toe server\n")
    port = int(input("Input port number\n"))
    
    #Set up server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((hostAddress, port))

    s.listen(1)

    #while True:
    print("Waiting for player to connect...")
    clientConnection, clientAddress = s.accept()

    #Recieve client username:
    clientUsernameData = clientConnection.recv(1024)
    clientUsername = clientUsernameData.decode()
    print(clientUsername + " has connected")

    #Send username to client
    serverUsername = "player2"
    clientConnection.send(serverUsername.encode())

    hostGamePlay(clientUsername, serverUsername, clientConnection)

    s.close()

if __name__ == "__main__":
    setUpGameServer()