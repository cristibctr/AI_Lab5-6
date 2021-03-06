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

    def clone(self):
        return State(list(self.balls))


class QAndA:
    state: State
    answer: int

    def __init__(self, state, answer):
        self.state = state
        self.answer = answer


class Game:
    FAILED_TO_GUESS = -1
    SUCCEEDED_TO_GUESS = -2
    GAME_ALREADY_ENDED = -3

    def __init__(self, n, m, k):
        self.allStates = []
        self.numberOfColors = n
        self.numberOfSameColoredBalls = m
        self.numberOfBallsInState = k
        self.possibleStates = self.getAllPossibleStates()
        self.finalState = self.chooseRandomState()
        self.ended = False

    def chooseRandomState(self):
        chosenColors = []

        while len(chosenColors) < self.numberOfBallsInState:
            randColor = random.randrange(self.numberOfColors)

            if self.numberOfSameColoredBalls > chosenColors.count(randColor):
                chosenColors.append(randColor)

        return State(chosenColors)

    def isFinal(self, qa: QAndA):
        if qa.state.availableTries <= 0:
            return Game.FAILED_TO_GUESS
        if self.numberOfBallsInState == qa.answer:
            return Game.SUCCEEDED_TO_GUESS
        return 0

    def addState(self, qa: QAndA):
        if len(qa.state.balls) <= self.numberOfBallsInState:
            self.allStates.append(qa)

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

        qa = QAndA(state, self.countCorrectGuesses(state))

        self.addState(qa)

        final = self.isFinal(qa)

        if final == Game.FAILED_TO_GUESS or final == Game.SUCCEEDED_TO_GUESS:
            self.ended = True
            return final

        return qa.answer

    def getAvailableTries(self):
        if len(self.allStates) == 0:
            return self.numberOfColors * 2 - 1
        else:
            return self.allStates[-1].state.availableTries - 1

    def __str__(self) -> str:
        return f'Number of colors: {self.numberOfColors}\n' \
               f'There are {self.numberOfSameColoredBalls} balls for each color\n' \
               f'{self.numberOfBallsInState} balls were chosen'

    def okState(self, state: State) -> bool:
        for color in range(0, self.numberOfColors):
            if self.numberOfSameColoredBalls < state.balls.count(color):
                return False

        return True

    def backTrackStates(self, state, index) -> list[State]:
        if index == self.numberOfBallsInState:
            return [state]

        result = []

        for color in range(0, self.numberOfColors):
            newState: State = state.clone()
            newState.balls[index] = color
            if self.okState(state):
                result += self.backTrackStates(newState, index + 1)

        return result

    def getAllPossibleStates(self) -> list[State]:
        initialState = State([-1 for i in range(0, self.numberOfBallsInState)])

        return self.backTrackStates(initialState, 0)

# MARK -- Ck

def question(state: State, state1: State):
    correctGuesses = 0

    for index in range(0, min(len(state.balls), len(state1.balls))):
        if state.balls[index] == state1.balls[index]:
            correctGuesses += 1

    return correctGuesses


def eliminateImpossibleStates(possibleStates: list[State], qAndA: QAndA) -> list[State]:
    result = []

    for state in possibleStates:
        if question(state, qAndA.state) == qAndA.answer:
            result.append(state)

    return result


def possibleNextStates(allPossibleStates: [State], allQAndA: [QAndA]):
    possibleStates = list(allPossibleStates)

    for qAndA in allQAndA:
        possibleStates = eliminateImpossibleStates(possibleStates, qAndA)

    return possibleStates


# MARK -- es(q, C)

def estimate(forQuestion: State, possibleStates: list[State], previousMinimum: int):
    minim = previousMinimum

    for answer in reversed(range(0, len(forQuestion.balls) + 1)):
        resultingStates = possibleNextStates(possibleStates, [QAndA(forQuestion, answer)])

        count = len(resultingStates)

        if count:
            if count < previousMinimum:
                return count

            if count < minim:
                minim = count

    return minim


# MARK - le(q, C) = es(q, C) when est(C) = len(C)
#
# FOR MINIMAX WITHOUT APLHA-BETA PRUNNING
#
# def permutations(forQuestion: State, possibleStates: list[State]):
#     result = []
#
#     for answer in range(0, len(forQuestion.balls) + 1):
#         resultingStates = possibleNextStates(possibleStates, [QAndA(forQuestion, answer)])
#
#         if len(resultingStates):
#             result.append(resultingStates)
#
#     return result
#
#
# def estimate(forQuestion: State, possibleStates: list[State]):
#     maxim = 0
#
#     for dqa in permutations(forQuestion, possibleStates):
#         if len(dqa) > maxim:
#             maxim = len(dqa)
#
#     return 1 + maxim


# MARK - F(q1, a1, ...)

def bestStates(possibleStates: list[State]):
    result = []
    maxim = 0

    for q in possibleStates:
        es = estimate(q, possibleStates, len(possibleStates))

        if es > maxim:
            result.clear()
            maxim = es

        if es == maxim:
            result.append(q)

    return result


# MARK - fk+1(q1, a1, ...)

def getNextQuestion(possibleStates: list[State]):
    return bestStates(possibleStates)[0]


def manual(newGame: Game):

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

        # print(permutations())


def minimax(newGame: Game):

    print(f"DELETE THIS: final state is: {newGame.finalState}")

    print(newGame)

    print("Try guessing the chosen balls by entering the colors as numbers with spaces in between\n")
    while True:
        remainingStates = possibleNextStates(newGame.possibleStates, newGame.allStates)

        bestQuestion = getNextQuestion(remainingStates)

        print(bestQuestion)

        guessResult = newGame.makeGuess(bestQuestion)

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


if __name__ == '__main__':
    newGame = Game(5, 5, 5)

    doItManual = False

    if doItManual:
        manual(newGame)
    else:
        minimax(newGame)

    print("Game ended!\n")










# returns number of possible outcomes when you guessed x correct balls starting from current state
def numberOfPossibilities(game, state, correctGuesses):
    # took me more than an hour to define this formula using many examples ---- not sure if it's correct
    return (pow(game.numberOfColors, len(state.balls) - correctGuesses) - (
                len(state.balls) - correctGuesses)) * math.comb(len(state.balls), correctGuesses) - 1


# generates the number of possible outcomes for every possible number of correct guesses
def generateAllGuesses(game, state):
    genNr = []
    for correctGuesses in range(0, len(state.balls)):
        genNr.append(numberOfPossibilities(game, state, correctGuesses))
    return genNr


def generateAllStates(game):
    possibleStates = list(product([i for i in range(1, game.numberOfColors + 1)], repeat=game.numberOfBallsInState))
    for state in possibleStates:
        print(generateAllGuesses(game, State(state)))
