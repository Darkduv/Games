from super_matrix import *
# Todo : TwoPlayersGame, EvalFunction, Player, Situation


class Player:

    def __init__(self, name=""):
        self.name = name
        self._nb_victory = 0

    def p4_play(self):
        return self.name, "Zut"

    def one_more_victory(self):
        self._nb_victory += 1

    @property
    def info_victories(self):
        return self.name + " has won " + str(self._nb_victory) + " victories"


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__("Computer")


class TwoPlayerGame:

    def __init__(self):
        self.current_situation = Situation()


class Situation:

    def __init__(self):
        self.state = SuperMatrix()

    def __str__(self):
        return self.state.__str__()





