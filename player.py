"""
Class for each player
"""

class Player:
    board = None
    
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
