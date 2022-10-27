"""Some Tools for game mechanics, not gui : game base class, historic.."""

__all__ = ['EmptyHistoric', 'EmptyHistoricError',
           'InvalidAction', 'InvalidActionError',
           'SimpleHistoric', 'GameNPlayer']

from abc import ABC, abstractmethod


class EmptyHistoricError(Exception):
    """Raise when trying accessing a value of an empty historic"""


class InvalidActionError(Exception):
    """Raise when trying to make an invalid action"""


EmptyHistoric = EmptyHistoricError()
InvalidAction = InvalidActionError()


class SimpleHistoric:
    """For keeping track of the actions"""

    def __init__(self, l_saves: list = None, current_undo: list = None):
        if l_saves is None:
            l_saves = []
        if current_undo is None:
            current_undo = []
        self.l_saves = l_saves
        self.current_undo = current_undo

    def save_new(self, save):
        """Save a state or an action"""
        self.l_saves.append(save)
        self.current_undo = []

    def undo(self):
        if not self.l_saves:
            raise EmptyHistoric
        save = self.l_saves.pop(-1)
        self.current_undo.append(save)
        return save

    def redo(self):
        if not self.current_undo:
            raise EmptyHistoric
        save = self.current_undo.pop(-1)
        self.l_saves.append(save)
        return save


class GameNPlayer(ABC):
    """Skeleton of a game of N players"""

    def __init__(self, nb_players=2):
        self.nb_players = nb_players
        self.player = 0  # player currently playing
        self.turn = 0  # nb round/turn

    @abstractmethod
    def play(self, action) -> bool:
        """Must implement the given action. Return if the player wins."""

    @abstractmethod
    def can_play(self) -> bool:
        """Can the current player play ?"""

    @abstractmethod
    def possible_actions(self):
        """Get the possibles actions for the current player"""

    @abstractmethod
    def win(self, action) -> int:
        """if winning, return the id of the player winning. else -1"""

    def next_player(self):
        """Update new id player"""
        self.player += 1
        self.player %= self.nb_players

    def undo_action(self, action):
        """ Undo the action """
        raise NotImplemented

    def redo_action(self, action_or_state):
        """ Redo the action """
        raise NotImplemented

    def apply(self, state_saved):
        """Set game to the given state"""
        raise NotImplemented

    @abstractmethod
    def init_game(self, *args, **kwargs):
        """ (Re) initialize the game """

    def copy(self) -> "GameNPlayer":
        """ Copy the object """
        raise NotImplemented

    def export_save(self):
        """ Export/Save the game in a lighter way than copying"""
        raise NotImplemented
