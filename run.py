import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip
import os
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('personal-budget')


class ClearDisplayMixin:
    def clear_display(self):
        os.system('clear')

class Budget(ClearDisplayMixin):
    """
    Budget class that handles user option for calculations.
    """
    def __init__(self):
        self.plan = self.choose_budget_plan()
        self.income = self.enter_income()
        self.currency = self.choose_currency()
        self.clear_display()
        self.update_income()
        
    
    def choose_budget_plan(self):
        """
        Gets user input for budget plan based on menu presented on the screen, validates the choice, clears terinal and returns user's choice.
        """
        response = pyip.inputMenu(['50/30/20', '70/20/10', 'About plans'], numbered=True)
        return response

    def enter_income(self):
        """
        Gets user's input for income, validates the choice, clears terinal and returns user's choice.
        """
        income = pyip.inputFloat("Enter your monthly income (-TAX): \n")
        return income
    
    def choose_currency(self):
        """
        Gets user's input for currency based on menu presented on the screen, validates the choice, clears terinal and returns user's choice.
        """
        currency = pyip.inputMenu(['PLN', 'EUR', 'GBP', 'USD'], prompt="Enter your currency: \n",  numbered=True)
        return currency

    def update_income(self):
        """
        Updates Google Sheet with user input income based on present month.
        """
        current_month = datetime.now().strftime('%B').lower()
        months = SHEET.worksheet('general').col_values(1)
        cell = SHEET.worksheet('general').find(current_month)
        
        SHEET.worksheet('general').update_cell(cell.row, cell.col+1, self.income)
    
    

class Savings(Budget, ClearDisplayMixin):
    """
    Budget child class to handle savings calculations.
    """

    def calculate_savings(self):
        """
        Calculates how much money is stored as Savings based on user's choice of budget plan.
        """
        if self.plan == "50/30/20":
            return self.income * 0.2
        elif self.plan == "70/20/10":
            return self.income * 0.1
        else:
            raise TypeError("Incorrect type for plan argument")
        self.clear_display()



save = Savings()
cal_save = save.calculate_savings()
print(cal_save)