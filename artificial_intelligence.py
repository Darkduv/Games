from SuperMatrix import *
# Todo : TwoPlayersGame, EvalFunction, Player, Situation


class Player:

    def __init__(self, name=""):
        self.name = name

    def p4_play(self):
        return self.name, "Zut"


class ComputerPlayer(Player):
    def __init__(self):
        Player.__init__(self, "Computer")


class TwoPlayerGame:

    def __init__(self):
        self.current_situation = Situation()


class Situation:

    def __init__(self):
        self.state = SuperMatrix()

    def __str__(self):
        return self.state.__str__()





