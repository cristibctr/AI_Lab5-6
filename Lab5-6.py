import random

class State:
    def __init__(self, balls = []):
        self.balls = balls
        self.availableTries = None

    def addTries(self, availableTries):
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
        self.ended = False

    def chooseRandomState(self):
        chosenColors = []
        while len(chosenColors) < self.k:
           randColor = random.randrange(self.n)
           if self.m > chosenColors.count(randColor):
               chosenColors.append(randColor)
        return State(chosenColors)

    def isFinal(self, state: State):
        if state.availableTries <= 0:
            return -1
        if self.finalState == state:
            return 1
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

    def makeGuess(self, state: State):
        if self.ended:
            print("Game ended. You can't continue playing!")
            return -1
        if len(self.allStates) == 0:
            state.addTries(self.n*2 - 1)
        else:
            state.addTries(self.allStates[-1].availableTries - 1)
        self.addState(state)
        if self.isFinal(state) == 1:
            print(f'You win!\n')
            self.ended = True
            return 1
        if self.isFinal(state) == -1:
            print('You lost the game :(\n')
            self.ended = True
            return -1
        if self.isFinal(state) == 0:
            print(f'You guessed {self.countCorrectGuesses(state)} out of {self.k}\n')
            print(f'You have {self.allStates[-1].availableTries} tries left\n')
            return 0
            
        

    def __str__(self) -> str:
        finalStr = f'Final state: {self.finalState}\n'
        for state in self.allStates:
            finalStr += state.__str__()
        return finalStr

if __name__ == '__main__':
    newGame = Game(8, 4, 4)
    print(newGame)
    while True:
        arr = input("Input your colors as numbers\n")
        colors = list(map(int,arr.split(' ')))
        guessResult = newGame.makeGuess(State(colors))
        if guessResult == 1 or guessResult == -1:
            break
