"""
Class for each player
"""

class Player:
    board = None
    beforeBonus = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes"]
    afterBonus = ["One pair", "Two pair", "Three-of-a-kind", "Four-of-a-kind", \
                  "Small straight", "Large straight", "House", "Chance", "Yatzy", "Total"]

    def __init__(self, name):
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

    def __str__(self):
        name = self.get("Participants")
        return f"Player {name}"

    def set(self, key, toWhat):
        """
        Sets board[key] = toWhat. If key is int, get corresponding key to index.
        """
        if type(key) is str:
            self.board[key] = toWhat
        elif type(key) is int:
            strKey = rowIndexToKey(key)
            self.board[strKey] = toWhat
        else:
            raise SystemExit

    def get(self, key):
        return self.board[key]

    def getName(self):
        return self.board["Participants"]

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
