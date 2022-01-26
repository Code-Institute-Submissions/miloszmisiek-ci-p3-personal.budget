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
MONTH_NOW = datetime.now().strftime('%B').lower()


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
        self.update_worksheet('general', self.income, MONTH_NOW, 'monthly income')
        
    
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

    def update_worksheet(self, worksheet, value, row, column):
        """
        Updates Google Sheet worksheet based on present month, value and column arguments.
        """
        print(f"Updating {column} in spreadsheet...\n")
        month_cell = SHEET.worksheet(worksheet).find(row)
        month_income = SHEET.worksheet(worksheet).find(column)
        SHEET.worksheet(worksheet).update_cell(month_cell.row, month_income.col, value)
        print(f"{column.capitalize()} updated successfully!\n")
    
    

class Savings(Budget, ClearDisplayMixin):
    """
    Budget child class to handle savings calculations.
    """

    def calculate_savings(self):
        """
        Calculates how much money is stored as Savings based on user's choice of budget plan.
        """
        if self.plan == "50/30/20":
            return round(self.income * 0.2, 1)
        elif self.plan == "70/20/10":
            return round(self.income * 0.1, 1)
        else:
            raise TypeError("Incorrect type for plan argument")
        self.clear_display()



save = Savings()
cal_save = save.calculate_savings()
save.update_worksheet('general', cal_save, MONTH_NOW, 'savings')