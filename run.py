import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip
import os
from datetime import datetime

# Global Variables for Google API
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('personal-budget')

# Global Variables for app processes
MONTH_NOW = datetime.now().strftime('%B').lower()


class ClearDisplayMixin:
    """
    Mixin to celar terminal screen.
    """
    def clear_display(self):
        os.system('clear')

class Budget(ClearDisplayMixin):
    """
    Budget class that handles user option for calculations.
    """
    def __init__(self):
        self.income = self.enter_income()
        self.plan_elements = self.choose_budget_plan()
        # self.currency = self.choose_currency()
        self.clear_display()
        self.update_worksheet_cell('general', self.income, MONTH_NOW, 'monthly income')
        
    
    def choose_budget_plan(self):
        """
        Gets user input for budget plan based on menu presented on the screen, validates the choice, clears terinal and returns user's choice.
        """
        while True:
            response = pyip.inputMenu(['50/30/20', '70/20/10', 'About plans'], prompt="Please select which budget plan you choose:\n", numbered=True)
            if response == '50/30/20':
                needs = round(self.income * 0.5, 1)
                wants = round(self.income * 0.3, 1)
                savings = round(self.income * 0.2, 1)
                break
            elif response == '70/20/10':
                needs = round(self.income * 0.7, 1)
                wants = round(self.income * 0.2, 1)
                savings = round(self.income * 0.1, 1)
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

    def update_worksheet_cell(self, worksheet, value, row, column):
        """
        Updates Google Sheet worksheet based on present month, value and column arguments.
        """
        print(f"Updating {column} in spreadsheet...\n")
        month_cell = SHEET.worksheet(worksheet).find(row)
        month_income = SHEET.worksheet(worksheet).find(column)
        SHEET.worksheet(worksheet).update_cell(month_cell.row, month_income.col, value)
        print(f"{column.capitalize()} updated successfully!\n\n")
    
class Savings(Budget, ClearDisplayMixin):
    """
    Budget child class to handle savings calculations.
    """
    def __init__(self, money):
        self.money = money
        self.update_worksheet_cell('general', self.money, MONTH_NOW, 'savings')

class Needs(Budget, ClearDisplayMixin,):
    """
    Budget child class to handle Needs calculations.
    """
    def __init__(self, money):
        self.money = money
        self.categories_string = self.create_needs_categories()
        self.categories_list = self.update_needs_categories(self.categories_string)

    def create_needs_categories(self):
        """
        Gets user input to create peronsalized categories or use default option. Validates inputs.
        """
        needs__options_menu = pyip.inputMenu(['Default', 'Create Categories'], prompt="Select how you want to manage your Needs:\n", numbered=True)
        if needs__options_menu == 'Create Categories':
            print("\nEnter your categories WITHOUT whitespaces such as spaces or tabs and seperated with commas.\n")
            print("Limit your categories to one word only\n")
            print("Example: Vehicle,Apartment,School,Bank")
            commas = False
            while not commas:
                user_needs_categories = pyip.inputStr(prompt="\nEnter your categories:\n", blockRegexes = ' ')
                if (user_needs_categories.find(',') != -1):
                    commas = True
                else:
                    print("\nYour inputs must be seperated with commas! Try again.")
            return user_needs_categories

    def update_needs_categories(self, needs_cat):
        """
        Updates NEEDS worksheet with categories of user's choice.
        """
        split_categories = needs_cat.split(',')
        month_row = SHEET.worksheet('needs').find('month')
        for num, item in enumerate(split_categories):
                SHEET.worksheet('needs').update_cell(month_row.row, num+2, item)
        return split_categories
        
    def input_values_for_needs(self):
        spendings = {}
        for item in self.categories_list:
            spendings[item] = pyip.inputFloat(prompt=f"Enter value for {item}: \n")
        
        return(spendings)



budget = Budget()
# save = Savings(budget.plan_elements[3])

needs = Needs(budget.plan_elements[1])
needs.input_values_for_needs()


