"""Implement some base class/objects for gui for coding games"""

__all__ = ["RecursiveMenuBar"]

import tkinter


class RecursiveMenuBar(tkinter.Menu):
    """Define recursively a menu with cascade submenus"""

    def __init__(self, root=None):
        super().__init__(root)
        root.config(menu=self)

    def config_menu(self, hierarchy, parent: tkinter.Menu = None):
        if parent is None:
            parent = self
            # underline = 0
        else:
            # underline = None
            pass

        for option in hierarchy:
            if option is None:
                parent.add_separator()
                continue
            label, menu_command = option

            if isinstance(menu_command, list):
                menu = tkinter.Menu(parent, tearoff=0)
                self.config_menu(menu_command, parent=menu)
                parent.add_cascade(label=label, menu=menu)
            else:
                parent.add_command(label=label, command=menu_command)
