import random

class Dice:
    dice = None

    def __init__(self):
        self.dice = [0]*5

    def __str__(self):
        result = "Dice rolls:"
        for i in range(len(self.dice)):
            result += f"\n    - Dice {i+1}: {self.dice[i]}"
        return result

    def setDiceTo(self, list):
        """
        Set "dice" to values in "list". For testing purposes
        """
        self.dice = list
        self.dice.sort()

    def roll(self, keepDice=[]):
        """
        Rolls all 5 dice to a number between 1-6, and return the dice list
        """
        dice = self.dice
        for i in range(len(dice)):
            if str(i+1) not in keepDice:
                dice[i] = random.randint(1, 6)
        dice.sort()
        return dice

    def calculateSum(self, whatType):
        """
        Calls on the correct function to calculate the sum of dice roll
        """
        sum = 0
        if whatType == "Aces":
            sum = self.sumOfDice(1)
        elif whatType == "Twos":
            sum = self.sumOfDice(2)
        elif whatType == "Threes":
            sum = self.sumOfDice(3)
        elif whatType == "Fours":
            sum = self.sumOfDice(4)
        elif whatType == "Fives":
            sum = self.sumOfDice(5)
        elif whatType == "Sixes":
            sum = self.sumOfDice(6)
        elif whatType == "One pair":
            sum = self.sumPair(1)
        elif whatType == "Two pair":
            sum = self.sumPair(2)
        elif whatType == "Three-of-a-kind":
            sum = self.sumNumOfAKind(3)
        elif whatType == "Four-of-a-kind":
            sum = self.sumNumOfAKind(4)
        elif whatType == "Small straight":
            sum = self.sumStraight()
        elif whatType == "Large straight":
            sum = self.sumStraight()
        elif whatType == "House":
            sum = self.sumHouse()
        elif whatType == "Chance":
            sum = self.sumOfDice(0) # Sum of all dice
        elif whatType == "Yatzy":
            sum = self.sumNumOfAKind(5) # 5-of-a-kind
            if sum != 0:
                sum = 50 # Yatzy -> 50 points
        else:
            raise SystemExit
        return sum

    def sumOfDice(self, ofType):
        """
        Returns the sum of numbers in the list dice, where the numbers == ofType.
        If ofType == 0, then return sum of all dice
        """
        sum = 0
        for number in self.dice:
            if ofType == 0:
                sum += number
            elif number == ofType:
                sum += number
        return sum

    def sumPair(self, howManyPairsLeft, ignoreNumber=0):
        """
        Returns the sum of "howManyPairsLeft" pairs. If ignoreNumber != 0, then ignore any
        possible pair containing that number
        """
        sum = 0
        previous = -1
        # Iterating trough dice in reverse (largest number first)
        for i in range(len(self.dice)-1, -1, -1):
            current = self.dice[i]
            if ignoreNumber == current:
                # Ignore current
                previous = -1
                continue
            if previous == current:
                # We have a pair
                if howManyPairsLeft == 1:
                    return sum + current * 2
                # At least 1 more pair
                sum += current * 2
                howManyPairsLeft -= 1
                previous = -1 # So current can't count towards another pair
                continue
            # Keep current for next iteration as previous
            previous = current

        # There were 0 pairs
        return 0

    def sumNumOfAKind(self, numOfAKind):
        """
        Returns the sum of "numOfAKind" dices that have the same value
        """
        sum = 0
        previous = []
        # Iterating trough dice in reverse (largest number first)
        for i in range(len(self.dice)-1, -1, -1):
            current = self.dice[i]
            if len(previous) == 0:
                previous.append(current)
            elif len(previous) == numOfAKind:
                # We have the required amount of a kind
                return previous[0] * numOfAKind
            elif current in previous:
                previous.append(current)
            else:
                # Current is not in previous
                previous.clear() # can clear since dice list is sorted
                previous.append(current)

        if len(previous) == numOfAKind:
            # Testing here too in case last number fulfilled the requirement
            return previous[0] * numOfAKind
        # There were 0 pairs
        return 0

    def sumStraight(self):
        """
        Returns the sum of a small/large straight, or 0 if there were no straight
        """
        previous = -1
        startNum = 0
        for number in self.dice:
            if previous == -1:
                # Start case
                previous = number
                startNum = number
            else:
                if number == previous + 1:
                    previous = number
                else:
                    # Not a straight
                    return 0

        if startNum == 1:
            return 15 # 1+2+3+4+5
        elif startNum == 2:
            return 20 # 2+3+4+5+6
        raise SystemExit

    def sumHouse(self):
        """
        Returns the sum of three-of-a-kind and a pair only if both are present, otherwise retun 0
        """
        sumThreeOfAKind = self.sumNumOfAKind(3)
        if self.sumNumOfAKind(5) != 0:
            # Pair containing same number as in threeOfAKind is ok
            sumPair = self.sumPair(1)
        else:
            # Ignore possible pairs containing sumThreeOfAKind/3
            sumPair = self.sumPair(1, sumThreeOfAKind/3)
        if sumPair == 0 or sumThreeOfAKind == 0:
            return 0
        return sumThreeOfAKind + sumPair

    def whatToKeep(self, whatType, moves):
        """
        Determines what dice should be kept before next throw, when one already knows
        which category one intends to put points in.
        Paramters:
            - whatType (str): Category for score, for ex. "Aces", "One pair", etc.
            - moves (int): How many remaining throws
        Return:
            - list of dices to keep before next throw (ex: ["1", "2", "5"], or ["0"] to end turn)
        """
        toKeep = [] # Keep list of dice numbers, not dice values
        dice = self.dice

        types = {"Aces": 1, "Twos": 2, "Threes": 3, "Fours": 4, "Fives": 5, "Sixes": 6}
        if whatType in types.keys():
            # Handles all categories in types.keys()
            for key, value in types.items():
                if whatType == key:
                    toKeep.extend(self.diceNumbersEqualTo(value))

        elif whatType == "One pair":
            # Test for any pair, and only keep pair of 4 or higher
            if self.sumPair(1) >= 8:
                toKeep.append("0") # Keep pair and end turn
            else:
                for i in range(len(dice)):
                    if dice[i] >= 4:
                        toKeep.append(i + 1)
                if [3, 4, 5] == toKeep:
                    # If all three dice numbers are in toKeep, remove dice 3 (number 4)
                    toKeep.pop(0)
        elif whatType == "Two pair":
            sumTwoPair = self.sumPair(2)
            if sumTwoPair > 0:
                # There is two pairs, keep current dice setup
                toKeep.append(0)
            else:
                sumPair = self.sumPair(1)
                if sumPair > 0:
                    value = sumPair / 2
                    # Keep dice with value of pair, plus the highest value dice not in a pair
                    addedOne = False
                    for i in range(4, -1, -1):
                        if dice[i] == value:
                            toKeep.append(i+1)
                        elif addedOne == False:
                            toKeep.append(i+1)
                            addedOne = True
                else:
                    # No pairs, keep the 2 highest value dice
                    toKeep.append(4); toKeep.append(5)
        elif whatType == "Three-of-a-kind":
            sum = self.sumNumOfAKind(3)
            if sum > 0:
                # Three-of-a-kind, keep
                toKeep.append(0)
            else:
                sum = self.sumPair(1)
                if sum > 0:
                    toKeep.extend(self.diceNumbersEqualTo(sum / 2))
                else:
                    toKeep.append(5)
        elif whatType == "Four-of-a-kind":
            sum = self.sumNumOfAKind(4)
            if sum > 0:
                # Four-of-a-kind, keep
                toKeep.append(0)
            else:
                sum = self.sumNumOfAKind(3)
                if sum > 0:
                    toKeep.extend(self.diceNumbersEqualTo(sum / 3))
                else:
                    sum = self.sumPair(1)
                    if sum > 0:
                        toKeep.extend(self.diceNumbersEqualTo(sum / 2))
                    else:
                        toKeep.append(5)
        elif whatType == "Small straight":
            smallStraight = [1, 2, 3, 4, 5]
            for i in range(len(dice)):
                if dice[i] in smallStraight:
                    toKeep.append(i+1)
                    # Only want 1 of each value, so remove it from list
                    smallStraight.remove(dice[i])
            if toKeep == [1, 2, 3, 4, 5]:
                toKeep.clear()
                toKeep.append(0)
        elif whatType == "Large straight":
            largeStraight = [2, 3, 4, 5, 6]
            for i in range(len(dice)):
                if dice[i] in largeStraight:
                    toKeep.append(i+1)
                    # Only want 1 of each value, so remove it from list
                    largeStraight.remove(dice[i])
            if toKeep == [1, 2, 3, 4, 5]:
                toKeep.clear()
                toKeep.append(0)
        elif whatType == "House":
            sumHouse = self.sumHouse()
            if sumHouse > 0:
                toKeep.append(0)
            else:
                sum = self.sumNumOfAKind(4)
                if sum > 0:
                    toKeep.extend(self.diceNumbersEqualTo(sum / 4))
                else:
                    sum = self.sumPair(2)
                    if sum > 0:
                        valueLargePair = self.sumPair(1) / 2
                        valueSmallPair = (sum - valueLargePair*2) / 2
                        for i in range(len(dice)):
                            if dice[i] == valueLargePair or dice[i] == valueSmallPair:
                                toKeep.append(i+1)
                    else:
                        sum = self.sumNumOfAKind(3)
                        if sum > 0:
                            toKeep.extend(self.diceNumbersEqualTo(sum / 3))
                        else:
                            sum = self.sumPair(1)
                            if sum > 0:
                                toKeep.extend(self.diceNumbersEqualTo(sum / 2))
                            else:
                                for i in range(3, 5):
                                    if dice[i] > 3:
                                        toKeep.append(i+1)
        elif whatType == "Chance":
            for i in range(len(dice)):
                if dice[i] >= (5 if moves == 2 else 4):
                    toKeep.append(i+1)
        elif whatType == "Yatzy":
            sum = self.sumNumOfAKind(5)
            if sum > 0:
                toKeep.append(0)    # Yatzy!
            else:
                sum = self.sumNumOfAKind(4)
                if sum > 0:
                    toKeep.extend(self.diceNumbersEqualTo(sum / 4))
                else:
                    sum = self.sumNumOfAKind(3)
                    if sum > 0:
                        toKeep.extend(self.diceNumbersEqualTo(sum / 3))
                    else:
                        sum = self.sumPair(1)
                        if sum > 0:
                            toKeep.extend(self.diceNumbersEqualTo(sum / 2))
                        else:
                            toKeep.append(5)

        toKeep.sort()
        print("Keep dice number:", toKeep, "\n")
        # Convert int elements to str
        toKeep = [str(elem) for elem in toKeep]
        return toKeep

    def diceNumbersEqualTo(self, value):
        """
        Add all values in dice list that are equal to value, to a new list, and return it.
        Is a function because this exact format was used a lot in self.whatToKeep()
        Parameter:
            - value (int): Compare values in dice to this value
        Return:
            - list containing all dice numbers where the dice == value
        """
        list = []
        for i in range(len(self.dice)):
            if self.dice[i] == value:
                list.append(i+1)
        return list

    def determineNextMove(self, moves, chooseFrom):
        """
        Determines next move with the available information
        Paramters:
            - moves (int): how many remaining throws
            - chooseFrom (list): all unused row categories ("Aces", "Twos", etc.)
        Return:
            - list of dices to keep before next throw (ex: ["1", "2", "5"], or ["0"] to end turn)
        """
        return self.whatToKeep(chooseFrom[0], moves)
