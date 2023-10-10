"""Manipulates Tic-Tac-Toe board and player statistics.

Includes methods to reset board, set last player to make a turn, update game statistics
such as number of games played, wins, ties, and losses. Prints user stats, etc.

game = BoardClass(username, opponentUsername)
game.updateBoard(2, "X")
game.printBoard()
"""

class BoardClass:

    currBoard = []
    playerUsername = ""
    opponentUsername = ""
    lastTurn = ""
    gamesPlayed = 0
    numWins = 0
    numTies = 0
    numLosses = 0

    def __init__(self, username="", opponentUserName=""):
        """Make BoardClass object.
        
        Args:
        playerUsername: Player's username.
        opponentUsername: Opponent's username.
        currBoard: Current tic-tac-toe board status.
        lastTurn: Last username to make a move.
        gamesPlayed: Total number of games played.
        numWins: Total wins of player.
        numTies: Total number of ties between player and opponent.
        numLosses: Total losses of player.
        """
        self.playerUsername = username
        self.opponentUsername = opponentUserName
        self.currBoard = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.lastTurn = ""
        self.gamesPlayed = 0
        self.numWins = 0
        self.numTies = 0
        self.numLosses = 0

    def updateLastTurn(self, lastTurn: str):
        """Updates last player to make a turn.
        
        Args:
        lastTurn: Username of last player to make a turn.
        """
        self.lastTurn = lastTurn

    def updateGamesPlayed(self):
        """Increments number of games played by 1.
        """
        self.gamesPlayed += 1

    def updateWins(self):
        """Increments number of wins by 1.
        """
        self.numWins += 1

    def updateLosses(self):
        """Increments number of losses by 1.
        """
        self.numLosses += 1

    def updateTies(self):
        """Increments number of ties by 1.
        """
        self.numTies += 1

    def resetGameBoard(self):
        """Resets game board to empty board.
        """
        self.currBoard = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def updateBoard(self, inputLocation: int, symbol: str):
        """Places symbol onto board with user specified location.
        
        Args:
        inputLocation: A number from 1-9 corresponding to a square on a 3x3 board
        symbol: Symbol to place on that square, usually X or O
        """
        row = (inputLocation - 1) // 3
        column = (inputLocation - 1) % 3
        self.currBoard[row][column] = symbol

    def isWinner(self) -> bool:
        """Checks if a player won the game by looking for 3 of the same symbol in a row; 
        either horizontally, vertically, or diagonally.

        Returns:
        Boolean indicating is a player has won the game.
        """
        # Check rows for winner
        for row in self.currBoard:
            if (row[0] == row[1] == row[2]) and (row[0] != " "):
                return True
        # Check columns for winner
        for column in range(3):
            if (self.currBoard[0][column] == self.currBoard[1][column] == self.currBoard[2][column] and (self.currBoard[0][column] != " ")):
                return True
        # Check diagonals for winner
        if (self.currBoard[0][0] == self.currBoard[1][1] == self.currBoard[2][2]) and (self.currBoard[0][0] != " "):
            return True
        if (self.currBoard[0][2] == self.currBoard[1][1] == self.currBoard[2][0]) and (self.currBoard[0][2] != " "):
            return True
        return False

    def boardIsFull(self) -> bool:
        """Checks if board is full. If board is full, and there is no winner, there is a tie.
        
        Returns:
        Boolean value indicating if board is full.
        """
        for row in self.currBoard:
            for column in row:
                if column == " ":
                    return False
        return True

    def printBoard(self):
        """Prints current board.
        """
        for row in self.currBoard:
            print("|" + "|".join(row) + "|")
        
    def printInstructions(self):
        """Prints game instructions.
        """
        inputExample = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        print("Instructions--------------------------------")
        print("Enter number 1-9 corresponding to squares as shown below to place marker:")
        for row in inputExample:
            print("|" + "|".join(row) + "|")

    def printStats(self):
        """Prints game statistics.
        """
        print("Game Statistics:")
        print("Your username: " + self.playerUsername)
        print("Opponent's username: " + self.opponentUsername)
        print("Last move: " + self.lastTurn)
        print("Games played: " + str(self.gamesPlayed))
        print("Wins: " + str(self.numWins))
        print("Losses: " + str(self.numLosses))
        print("Ties: " + str(self.numTies))
    
    def getInput(self) -> str:
        """Gets location input from user.

        Returns:
        userInput: string of user input 1-9.
        """
        try:
            userInput = input("Enter your move (1-9)\n")
            if (int(userInput) < 1) or (int(userInput) > 9):
                raise ValueError
            row = (int(userInput) - 1) // 3
            column = (int(userInput) - 1) % 3
            if self.currBoard[row][column] != " ":
                raise Exception
        except ValueError:
            print("Invalid entry, try again")
            return BoardClass.getInput(self)
        except Exception:
            print("This spot is not empty, try again")
            return BoardClass.getInput(self)

        return userInput
    
    def gameOver(self) -> bool:
        """Checks if game is over.

        Returns:
        Boolean value indicating if game is over.
        """
        if BoardClass.isWinner(self) or BoardClass.boardIsFull(self):
            return True


