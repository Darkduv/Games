class Player:

    def __init__(self, name=""):
        self.name = name
        self.nb_victory = 0

    def one_victory_more(self):
        self.nb_victory += 1

    def __repr__(self):
        return self.name + " has won " + str(self.nb_victory) + " victories"


class SuperList(list):

    def __setitem__(self, key, value):
        try:
            list.__setitem__(self, key, value)
        except IndexError:
            self.append(value)
