"""
This module costains SystemMixin to execute methods
used to clear terminal and restart program.
"""
import os
import sys
import time
from termcolor import colored
import pyfiglet
import pyinputplus as pyip


class SystemMixin:
    """
    Mixin to clear terminal screen.
    """
    # @staticmethod
    def clear_display(self):
        """
        Method to clear the display - logo remains.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        # Concept for pyfiglet styling comes from
        # https://www.youtube.com/watch?v=U1aUteSg2a4
        print(colored(pyfiglet.figlet_format("budget manager",
                                             font="slant", justify="center",
                                             width=100), "green"))

    def restart_program(self):
        """
        Method to restart or quit the program.
        """
        # Code copied from
        # https://stackoverflow.com/questions/48129942/python-restart-program
        restart = pyip.inputYesNo("\nDo you want to go back to Main Menu? "
                                  "Type Yes or No:\n")

        if restart == "yes":
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            self.clear_display()
            print("\nThe programm will be closed...")
            print("\nSee you next time!")
            time.sleep(5)
            self.clear_display()
            sys.exit(0)
