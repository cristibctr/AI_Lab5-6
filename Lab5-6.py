import random

class State:
    def __init__(self, balls = [], availableTries = None):
        self.balls = balls
        self.availableTries = availableTries

    def __hash__(self):
        return hash(self.balls)

    def __eq__(self, other):
        return (self.balls == other.balls)

    def __str__(self) -> str:
        return f'Balls: {self.balls} | Available tries: {self.availableTries}\n'

class Game:
    def __init__(self, n, m, k):
        self.allStates = []
        self.n = n
        self.m = m
        self.k = k
        self.finalState = self.chooseRandomState()

    def chooseRandomState(self):
        chosenColors = []
        while len(chosenColors) < self.k:
           randColor = random.randrange(self.n)
           if self.m > chosenColors.count(randColor):
               chosenColors.append(randColor)
        return State(chosenColors)

    def isFinal(self, state: State):
        if self.finalState == state:
            return 1
        if state.availableTries < 0:
            return -1
        return 0

    def addState(self, state: State):
        if len(state.balls) <= self.k:
            self.allStates.append(state)

    def countCorrectGuesses(self, state: State):
        correctBallsNr = 0
        for ballNr in range(self.k):
            if self.finalState.balls[ballNr] == state.balls[ballNr]:
                correctBallsNr += 1
        return correctBallsNr

    def __str__(self) -> str:
        finalStr = f'Final state: {self.finalState}\n'
        for state in self.allStates:
            finalStr += state.__str__()
        return finalStr

newGame = Game(8, 4, 4)
newState = State([2, 3, 4, 5], 5)
newGame.addState(newState)
print(newGame)

print(newGame.countCorrectGuesses(newState))
