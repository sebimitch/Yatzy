"""
Class for each player
"""
import time

class Player:
    playerType = ""   # Human/bot
    board = None
    beforeBonus = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes"]
    afterBonus = ["One pair", "Two pair", "Three-of-a-kind", "Four-of-a-kind", \
                  "Small straight", "Large straight", "House", "Chance", "Yatzy", "Total"]
    unusedRows = [] # For free Yatzy
    yatzyType = ""  # Forced/Free

    def __init__(self, name, playerType, yatzyType):
        self.board = {
            "Participants": name,
            "Aces": None,
            "Twos": None,
            "Threes": None,
            "Fours": None,
            "Fives": None,
            "Sixes": None,
            "Sum": None,
            "Bonus": None,
            "One pair": None,
            "Two pair": None,
            "Three-of-a-kind": None,
            "Four-of-a-kind": None,
            "Small straight": None,
            "Large straight": None,
            "House": None,
            "Chance": None,
            "Yatzy": None,
            "Total": None
        }
        self.playerType = playerType
        self.unusedRows = self.beforeBonus + self.afterBonus
        self.unusedRows.pop()   # Remove "Total"
        self.yatzyType = yatzyType

    def __str__(self):
        name = self.get("Participants")
        return f"Player {name}"

    def set(self, key, toWhat):
        """
        Sets board[key] = toWhat. If key is int, get corresponding key to index.
        """
        if type(key) is str:
            self.board[key] = toWhat
            self.unusedRows.remove(key)
        elif type(key) is int:
            strKey = rowIndexToKey(key)
            self.board[strKey] = toWhat
            self.unusedRows.remove(key)
        else:
            raise SystemExit

    def get(self, key):
        return self.board[key]

    def getName(self):
        return self.board["Participants"]

    def getPlayerType(self):
        return self.playerType

    def getInput(self, inputText, dice, moves=0, category=""):
        """
        Depending on if current player is Human/Bot, ask for input() or time.sleep()
        Paramters:
            - inputText (str): Text to display in input(inputText)
            - dice (list): instance of Dice, contains current dice setup
            - moves (int): How many remaining throws
            - category (str): What category to play in, ex: "Aces", "One pair", etc.
        """
        if self.playerType == "Human":
            return input(inputText)
        elif self.playerType == "Bot":
            time.sleep(0.5)
            if inputText == "What dice would you like to keep (ex: 1 3 5)(0 to keep all): ":
                print("\nBot calulcating...")
                if self.yatzyType == "Forced":
                    return dice.whatToKeep(category, moves)
                else:
                    return dice.determineNextMove(moves, self.unusedRows)

    def checkIfUpdate(self):
        """
        Check if enough rows have been filled to fill in Sum, Bonus or Total.
        """
        for i in range(1, 16):
            key = self.rowIndexToKey(i)
            if self.get(key) is None:
                break
            elif i == 6:
                self.updateType("Sum")
                self.updateType("Bonus")
            elif i == 15:
                self.updateType("Total")

    def updateType(self, type):
        """
        Calculate and fill in the cells of type: "Sum", "Bonus", "Total" when needed
        """
        sum = 0
        if type == "Sum":
            sum = self.calculateSumOfList(self.beforeBonus)
        elif type == "Bonus":
            if self.board["Sum"] >= 63:
                sum = 50
        elif type == "Total":
            sum = self.calculateSumOfList(self.beforeBonus)
            sum += self.calculateSumOfList(self.afterBonus)
        self.board[type] = sum

    def calculateSumOfList(self, list):
        sum = 0
        for key in list:
            value = self.board[key]
            if value is not None:
                sum += value
        return sum

    def checkIfRowAvailable(self, index):
        """
        Determines if the value corresponding to the index has already been filled.
        Returns True if row has not been filled.
        """
        key = self.rowIndexToKey(index)
        rowValue = self.board[key]
        return True if rowValue is None else False

    def rowIndexToKey(self, i):
        """
        Given a row index (1-15), return the type of yatzy score in str
        """
        # if
        if i <= 6:
            return self.beforeBonus[i-1]
        else:
            return self.afterBonus[i-7]
