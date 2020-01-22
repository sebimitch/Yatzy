"""
My implementation of the dice game Yatzy, as a text game
"""

from player import Player
from dice import Dice
import time

countHumanPlayers = -1
countBotPlayers = -1
yatzyType = ""  # free/forced
players = []
botNames = ["LazyBot", "SmartBot", "DogBot", "CatBot"]
rowIndexList = ["Index", 1, 2, 3, 4, 5, 6, "", "", 7, 8, 9, 10, 11, 12, 13, 14, 15, ""]
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
            countHumanPlayers = int(input("\nHow many human players? (1-4) "))
        except ValueError:
            continue

    # Ask for a name for each human player, and add a Player()
    for i in range(countHumanPlayers):
        while True:
            name = input(f"\nName of player {i+1}: ")
            if name != "":
                players.append(Player(name))
                break

    # Find how many machine players
    if countHumanPlayers != maxPlayers:
        maxMachinePlayers = maxPlayers - countHumanPlayers
        while (countBotPlayers < 0) or (countBotPlayers > maxMachinePlayers):
            try:
                countBotPlayers = int(input(f"\nHow many machine players? (0-{maxMachinePlayers}) "))
            except ValueError:
                continue

    # Adds a Player() for each bot
    for i in range(countBotPlayers):
        players.append(Player(botNames[i]))

    # Find yatzy type to play
    s = "\nGame type?\n  - Forced Yatzy: Player must follow game board (1's, then 2's,"
    print(s + " etc.)\n  - Free Yatzy: Player can choose what row to assign score to")
    while yatzyType != "free" and yatzyType != "forced":
        yatzyType = input("\nPlay 'free' or 'forced' Yatzy? ")

def printBoard():
    """
    Prints the yatzy board
    """
    board = []

    keyList = list(combinations.keys())
    widthKey = findMinWidth(keyList)
    widthIndex = findMinWidth(rowIndexList)

    for key in combinations:
        board.append(f"| {key:{widthKey}} |")

    for i in range(len(board)):
        # Write the index column
        rowIndex = rowIndexList[i]
        board[i] = f"| {rowIndex:<{widthIndex}} " + board[i]
        for player in players:
            # Write a column for each player
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
    for item in list:
        item = str(item) # Can't use len() on int
        if len(longest) < len(item):
            longest = item
    return len(longest)

def startGame():
    print("\n\n\n*** Starting game of Yatzy ***")
    dice = Dice()
    if yatzyType == "forced":
        forcedYatzy(dice)
    else:
        freeYatzy(dice)

def forcedYatzy(dice):
    for key in combinations:
        if key == "Participants":
            continue
        # Each player plays on each row
        for player in players:
            printBoard()
            if key in ["Sum", "Bonus", "Total"]:
                player.updateType(key)
                input("\nPress ENTER to continue: ")
                continue

            # Each player has up to 3 throws
            for turn in range(1, 4):
                print(f"\nIt's player {player.getName()}'s turn: Throw {turn} (of 3)")
                print(f"Goal -> {key}: {combinations[key]}")
                if turn == 1:
                    input("Press ENTER to roll: ")
                    dice.roll()
                    print(dice)
                else:
                    toKeep = input("What dice would you like to keep (ex: 1 3 5)(0 to keep all): ").split()
                    if toKeep == ["0"]:
                        # Keep current dice setup
                        break
                    dice.roll(toKeep)
                    print(dice)

                input("\nPress ENTER to continue: ")

            # Player is finished with this turn
            player.set(key, dice.calculateSum(key))
    # Final score
    printBoard()

def freeYatzy(dice):
    # There are always 15 rows to fill in
    for i in range(15):
        # Each player plays once per row
        for player in players:
            printBoard()

            # Each player has up to 3 throws
            for turn in range(1, 4):
                print(f"\nIt's player {player.getName()}'s turn: Throw {turn} (of 3)")
                if turn == 1:
                    input("Press ENTER to roll: ")
                    dice.roll()
                    print(dice)
                else:
                    toKeep = input("What dice would you like to keep (ex: 1 3 5)(0 to finish turn): ").split()
                    if toKeep == ["0"]:
                        # Keep current dice setup
                        break
                    dice.roll(toKeep)
                    print(dice)
                input("\nPress ENTER to continue: ")
            # Turn finished, must now choose which row to score in
            rowIndex = -1
            while (rowIndex < 1 or rowIndex > 15):
                try:
                    rowIndex = int(input("\nChoose row index to set score: "))
                    if rowIndex < 1 or rowIndex > 15:
                        continue
                    rowIndex = rowIndex if player.checkIfRowAvailable(rowIndex) else -1
                except ValueError:
                    pass

            strKey = player.rowIndexToKey(rowIndex)
            player.set(strKey, dice.calculateSum(strKey))
            player.checkIfUpdate()
    # Final score
    printBoard()


if __name__ == "__main__":
    initiate()
    startGame()
