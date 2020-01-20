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
            "Participants": None,
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
        self.board["Participants"] = name

    def __str__(self):
        name = self.get("Participants")
        return f"Player {name}"

    def set(self, key, toWhat):
        """
        Sets board[key] = toWhat
        """
        self.board[key] = toWhat

    def get(self, key):
        return self.board[key]

    def getName(self):
        return self.board["Participants"]

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
