"""Client side player. symbol x/X

Asks player for host's address and port number. Asks for a username and sends it to host. Starts game 
having the user make the first move. Alternate moves between user and host until 
game is over. Asks player if they want to play again, then resets board or 
print statistics if player wants to stop playing.

"""

import socket
from BoardClass import BoardClass

def askForUsername() -> str:
    """Asks user for alphanumeric username.

    Returns:
    String of username.
    """
    try:
        username = input("Enter your username:\n")
        if (username.isalnum()):
            return username
        else:
            raise ValueError
    except:
        print("Username must consist of only letters or numbers. Please try again.")
        return askForUsername()
        
def askKeepPlaying() -> bool: 
    """Asks user if they want to play another game.

    Returns:
    Boolean that's True if player wnats to play again, False if not.
    """
    playAgain = input("Play again? Enter y/n\n")
    try:
        if playAgain.lower() == "y":
            return True
        elif playAgain.lower() == "n":
            return False
        else:
            raise Exception
    except:
        print("Invalid choice, try again. Enter \"y\" or \"n\".")
        return askKeepPlaying()

def gamePlay(clientUsername: str, hostUsername: str, s: socket):
    """Runs gameplay between client and host.
    
    Args:
    clientUsername: Client's username.
    hostUsername: Host server's username.
    s: Socket between client and host.
    """
    #Start gameplay
    gameInstance = BoardClass(clientUsername, hostUsername)
        
    #Start Game:
    gameInstance.printInstructions()
    player1Symbol = "X"
    player2Symbol = "O"
    keepPlaying = True
    while (keepPlaying):
        # Get client's move
        print("Your turn. Your marker is: " + player1Symbol)
        playerMove = gameInstance.getInput()
        s.send(playerMove.encode())
        # Update Board with user move and send to host
        gameInstance.updateBoard(int(playerMove), player1Symbol)
        print("Your move:")
        gameInstance.printBoard()
        # Update last person to make move
        gameInstance.updateLastTurn(clientUsername)

        #Check if game is over and then ask if player wants to keep playing
        #Update game stats
        if gameInstance.gameOver():
            gameInstance.updateGamesPlayed()
            if gameInstance.isWinner():
                print("You win!")
                gameInstance.updateWins()
            elif gameInstance.boardIsFull():
                print("You and " + hostUsername + " tied.")
                gameInstance.updateTies()
            keepPlaying = askKeepPlaying()
            if keepPlaying:
                print("Board Reset.")
                s.send(b"y")
                gameInstance.resetGameBoard()
                continue
            elif not keepPlaying:
                print("Disconnecting...")
                s.send(b"n")
                gameInstance.resetGameBoard()
                s.close()
                break
            
        # Get Host's move
        print("Waiting for " + hostUsername + "'s move...")
        hostMoveData = s.recv(1024)
        hostMove = hostMoveData.decode()
        # Update Board with host's move
        gameInstance.updateBoard(int(hostMove), player2Symbol)
        print(hostUsername + " has made a move:")
        gameInstance.printBoard()
        # Update last person to make move
        gameInstance.updateLastTurn(hostUsername)

        #Check if game is over and then ask if player wants to keep playing
        #Update game stats
        if gameInstance.gameOver():
            gameInstance.updateGamesPlayed()
            if gameInstance.isWinner():
                print("You lose.")
                gameInstance.updateLosses()
            elif gameInstance.boardIsFull():
                print("You and " + hostUsername + " tied.")
                gameInstance.updateTies()
            keepPlaying = askKeepPlaying()
            if keepPlaying:
                print("Board Reset.")
                s.send(b"y")
                gameInstance.resetGameBoard()
                continue
            elif not keepPlaying:
                print("Disconnecting...")
                s.send(b"n")
                gameInstance.resetGameBoard()
                s.close()
                break
    gameInstance.printStats()
    print("Goodbye!")

#Get host address and port information
def connectToHost() -> tuple:
    """Asks user for host information and establishes connection between client and host.
    Ask user for username, and get's host's username.

    Returns:
    Tuple of client's username, host's username, and socket object."""
    try:
        hostAddress = input("Input host name or IP address of Player 2\n")
        port = int(input("Input port number\n"))

        #Connect to server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostAddress, port))
        print("Connected to host successfully")

        clientUsername = askForUsername()
        s.send(clientUsername.encode())

        #Receive server username
        hostUsernameData = s.recv(1024)
        hostUsername = hostUsernameData.decode()
        print("Host's username is: " + hostUsername)
        
    except:
        tryAgain = input("Connection Failed, Try Again? Enter y/n\n")
        while (tryAgain.lower() != "y" and tryAgain.lower() != "n"): #keep asking for input (case insensitive) until user enters y/n
            tryAgain = input("Connection Failed, Try Again? Enter y/n\n")
        if tryAgain == "y":
            connectToHost()
        else:
            print("Ending program")

    return (clientUsername, hostUsername, s)

if __name__ == "__main__":
    gameInfo = connectToHost()
    gamePlay(gameInfo[0], gameInfo[1], gameInfo[2])