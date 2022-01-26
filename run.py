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

class DistribiuteMoneyMixin:
    def calculate_money(self, multiplier):
        """
        Calculates how much money is stored as Savings based on user's choice of budget plan.
        """
        if self.plan_list[0] == "50/30/20":
            return round(self.income * multiplier, 1)
        elif self.plan_list[0] == "70/20/10":
            return round(self.income * multiplier, 1)
        else:
            raise TypeError("Incorrect type for plan argument")
    

class Budget(ClearDisplayMixin):
    """
    Budget class that handles user option for calculations.
    """
    def __init__(self):
        self.plan_list = self.choose_budget_plan()
        self.income = self.enter_income()
        # self.currency = self.choose_currency()
        self.clear_display()
        self.update_worksheet('general', self.income, MONTH_NOW, 'monthly income')
        
    
    def choose_budget_plan(self):
        """
        Gets user input for budget plan based on menu presented on the screen, validates the choice, clears terinal and returns user's choice.
        """
        while True:
            response = pyip.inputMenu(['50/30/20', '70/20/10', 'About plans'], prompt="Please select which budget plan you choose:\n", numbered=True)
            if response == '50/30/20':
                needs = 0.5
                wants = 0.3
                savings = 0.2
                break
            elif response == '70/20/10':
                needs = 0.7
                wants = 0.2
                savings = 0.1
                break
            else:
                self.clear_display()
                print("The 50/30/20 rule is a money management technique that divides your income into three categories:\n50% Needs(essentials)\n30% Wants(non-essentials)\n20% Savings.\n\nBy default this app provides following sub-categories:\nNeeds: Housing, Vehicle costs, Insurance, Food and Banking\nWants: Entertaintment, Wellbeing and Travel\n* Savings is what is meant to be left untouched and used only in case there is absolute need for it. It can cover any unexpected costs.\n\nThe 70/20/10 rule is less robust investment type, where the budget is split in proportion:\n70% Needs\n20% Wants\n10% Savings\n")
        return [response, needs, wants, savings]

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
        print(f"{column.capitalize()} updated successfully!\n\n")
    
class Savings(Budget, ClearDisplayMixin, DistribiuteMoneyMixin):
    """
    Budget child class to handle savings calculations.
    """
    def __init__(self, plan):
        self.plan = plan
        self.calc_save = self.calculate_money(self.plan)
        self.update_worksheet('general', self.calc_save, MONTH_NOW, 'savings')
        # self.clear_display()

class Needs(Budget, ClearDisplayMixin, DistribiuteMoneyMixin):
    """
    Budget child class to handle Needs calculations.
    """
    def __init__(self, plan):
        self.plan = plan
        self.calc_need = self.calculate_money(self.plan)
        # self.clear_display()



budget = Budget()
save = Savings(budget.plan_list[3])
need = Needs()