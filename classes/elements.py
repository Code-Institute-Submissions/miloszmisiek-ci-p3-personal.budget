"""
This module contains budget elements,
represented with classes:
- Savings
- Needs
- Wants
"""

from classes.systemmixin import SystemMixin
from classes.updatespreadsheetmixin import UpdateSpreadsheetMixin


class Savings(SystemMixin, UpdateSpreadsheetMixin):
    """
    Class to handle Savings calculations.
    """

    def __init__(self, money, month):
        self.month = month
        self.money = money
        self.update_worksheet_cell('general', self.money,
                                   self.month, 'Savings')
        self.update_worksheet_cell('general', '', self.month, 'Extra')


class Needs(SystemMixin, UpdateSpreadsheetMixin):
    """
    Class to handle Needs calculations.
    """

    def __init__(self, money):
        self.money = money
        self.categories_string = self.create_categories('needs',
                                                        'Housing,Vehicle,'
                                                        'Insurance,Food,'
                                                        'Banking')
        self.categories_list = self.update_worksheet_categories(
            self.categories_string, 'needs', 'Month')


class Wants(SystemMixin, UpdateSpreadsheetMixin):
    """
    Class to handle Wants calculations.
    """

    def __init__(self, money):
        self.money = money
        self.categories_string = self.create_categories(
            'wants', 'Enteraintment,Wellbeing,Travel')
        self.categories_list = self.update_worksheet_categories(
            self.categories_string, 'wants', 'Month')
