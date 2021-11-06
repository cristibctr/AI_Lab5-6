import random
import math
from itertools import product

class State:
    def __init__(self, balls=[]):
        self.balls = balls
        self.availableTries = None

    def setTries(self, availableTries):
        self.availableTries = availableTries

    def __hash__(self):
        return hash(self.balls)

    def __eq__(self, other):
        return (self.balls == other.balls)

    def __str__(self) -> str:
        return f'Balls: {self.balls} | Available tries: {self.availableTries}'


class Game:
    FAILED_TO_GUESS = -1
    SUCCEEDED_TO_GUESS = -2
    GAME_ALREADY_ENDED = -3

    def __init__(self, n, m, k):
        self.allStates = []
        self.numberOfColors = n
        self.numberOfSameColoredBalls = m
        self.numberOfBallsInState = k
        self.finalState = self.chooseRandomState()
        self.ended = False

    def chooseRandomState(self):
        chosenColors = []

        while len(chosenColors) < self.numberOfBallsInState:
            randColor = random.randrange(self.numberOfColors)

            if self.numberOfSameColoredBalls > chosenColors.count(randColor):
                chosenColors.append(randColor)

        return State(chosenColors)

    def isFinal(self, state: State):
        if state.availableTries <= 0:
            return Game.FAILED_TO_GUESS
        if self.finalState == state:
            return Game.SUCCEEDED_TO_GUESS
        return 0

    def addState(self, state: State):
        if len(state.balls) <= self.numberOfBallsInState:
            self.allStates.append(state)

    def countCorrectGuesses(self, state: State):
        correctBallsNr = 0
        for ballNr in range(self.numberOfBallsInState):
            if self.finalState.balls[ballNr] == state.balls[ballNr]:
                correctBallsNr += 1
        return correctBallsNr

    def makeGuess(self, state: State):
        if self.ended:
            return Game.GAME_ALREADY_ENDED

        state.setTries(self.getAvailableTries())

        self.addState(state)

        final = self.isFinal(state)

        if final == Game.FAILED_TO_GUESS or final == Game.SUCCEEDED_TO_GUESS:
            self.ended = True
            return final

        return self.countCorrectGuesses(state)

    def getAvailableTries(self):
        if len(self.allStates) == 0:
            return self.numberOfColors * 2 - 1
        else:
            return self.allStates[-1].availableTries - 1

    def __str__(self) -> str:
        return f'Number of colors: {self.numberOfColors}\n' \
               f'There are {self.numberOfSameColoredBalls} balls for each color\n' \
               f'{self.numberOfBallsInState} balls were chosen'


#returns number of possible outcomes when you guessed x correct balls starting from current state
def numberOfPossibilities(game, state, correctGuesses):
    #took me more than an hour to define this formula using many examples ---- not sure if it's correct
    return (pow(game.numberOfColors, len(state.balls) - correctGuesses) - (len(state.balls) - correctGuesses)) *  math.comb(len(state.balls), correctGuesses) - 1

#generates the number of possible outcomes for every possible number of correct guesses
def generateAllGuesses(game, state):
    genNr = []
    for correctGuesses in range(0, len(state.balls)):
        genNr.append(numberOfPossibilities(game, state, correctGuesses))
    return genNr

def generateAllStates(game):
    possibleStates = list(product([i for i in range(1, game.numberOfColors + 1)], repeat=game.numberOfBallsInState))
    for state in possibleStates:
        print(generateAllGuesses(game, State(state)))


if __name__ == '__main__':
    newGame = Game(5, 4, 4)


    generateAllStates(newGame)
    exit()

    print(f"DELETE THIS: final state is: {newGame.finalState}")

    print(newGame)

    print("Try guessing the chosen balls by entering the colors as numbers with spaces in between\n")
    while True:
        arr = input("Input your colors as numbers:\n")

        try:
            colors = list(map(int, arr.split(' ')))
        except Exception as e:
            print(f"Invalid input. Error: {e}\n")
            continue

        guessResult = newGame.makeGuess(State(colors))

        if guessResult == Game.SUCCEEDED_TO_GUESS:
            print("You did it!\n")
            print(f"You guessed {newGame.finalState}\n")
            break

        if guessResult == Game.FAILED_TO_GUESS:
            print("You failed to guess the colors!\n")
            print(f"The should have guessed {newGame.finalState}\n")
            break

        print(f"You have guessed {guessResult} balls out of {newGame.numberOfBallsInState}\n")
        print(f"You have {newGame.getAvailableTries() + 1} tries left\n")

    print("Game ended!\n")
