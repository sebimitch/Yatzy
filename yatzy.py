"""
My implementation of the dice game Yatzy, as a text game
"""

from player import Player

countHumanPlayers = -1
countBotPlayers = -1
yatzyType = ""  # free/forced
players = []
botNames = ["LazyBot", "SmartBot", "DogBot", "CatBot"]
combinations = {
    "Participants": "The names of participants",
    "Aces": "The sum of dice with number 1",
    "Twos": "The sum of dice with number 2",
    "Threes": "The sum of dice with number 3",
    "Fours": "The sum of dice with number 4",
    "Fives": "The sum of dice with number 5",
    "Sixes": "The sum of dice with number 6",
    "Sum": "Sum of above points",
    "Bonus": "If the sum is above 63, give a bonus of 50 points",
    "One pair": "Two similar dice",
    "Two pair": "Combination of two similar dice and two other similar dice",
    "Three-of-a-kind": "Three similar dice",
    "Four-of-a-kind": "Four similar dice",
    "Small straight": "Combination of dice with 1-2-3-4-5",
    "Large straight": "Combination of dice with 2-3-4-5-6",
    "House": "Combination of three-of-a-kind and a pair",
    "Chance": "Any combination",
    "Yatzy": "Five similar dice",
    "Total": "The total sum"
}

def initiate():
    """
    Asks user how many players, how many human/machine players, free or forced Yatzy...
    """
    global countHumanPlayers, countBotPlayers, yatzyType, players#, botNames
    maxPlayers = 4

    # Find how many human players
    while (countHumanPlayers < 1) or (countHumanPlayers > maxPlayers):
        try:
            countHumanPlayers = int(input("How many human players? (1-4) "))
        except ValueError:
            continue

    # Ask for a name for each human player, and add a Player()
    for i in range(countHumanPlayers):
        while True:
            name = input(f"Name of player {i+1}: ")
            if name != "":
                players.append(Player(name))
                break

    # Find how many machine players
    if countHumanPlayers != maxPlayers:
        maxMachinePlayers = maxPlayers - countHumanPlayers
        while (countBotPlayers < 0) or (countBotPlayers > maxMachinePlayers):
            try:
                countBotPlayers = int(input(f"How many machine players? (0-{maxMachinePlayers}) "))
            except ValueError:
                continue

    # Adds a Player() for each bot
    for i in range(countBotPlayers):
        players.append(Player(botNames[i]))

    # Find yatzy type to play
    while yatzyType != "free" and yatzyType != "forced":
        yatzyType = input("Play 'free' or 'forced' Yatzy? ")


def printBoard():
    """
    Prints the yatzy board
    """
    board = []

    keyList = list(combinations.keys())
    widthKey = findMinWidth(keyList)

    for key in combinations:
        board.append(f"| {key:{widthKey}} |")

    for i in range(len(board)):
        for player in players:
            item = player.get(keyList[i])
            if item == None:
                item = ""
            board[i] += f" {item:{widthKey}} |"

    widthColumn = findMinWidth(board)
    print("\n")
    for row in board:
        print("-" * widthColumn)
        print(row)
    print("-" * widthColumn)

def findMinWidth(list):
    """
    Finds and returns the length of the longest string in list
    Parameter: (list) containing strings
    Return: (int) length of longest string in list
    """
    longest = ""
    for str in list:
        if len(longest) < len(str):
            longest = str
    return len(longest)

def startGame():
    printBoard()

if __name__ == "__main__":
    initiate()
    startGame()