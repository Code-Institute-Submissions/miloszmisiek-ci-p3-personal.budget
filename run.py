import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip
import os
import pyfiglet
from termcolor import colored
from prettytable import PrettyTable
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
MONTH_NOW = datetime.now().strftime('%B')
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


class ClearDisplayMixin:
    """
    Mixin to clear terminal screen.
    """
    def clear_display(self):
        os.system('clear')
        # Concept for pyfiglet styling comes from https://www.youtube.com/watch?v=U1aUteSg2a4
        print(colored(pyfiglet.figlet_format("personal budget manager", font = "graceful", justify="center", width=110), "green"))

class UpdateSpreadsheetMixin:
    """
    Mixin for functions related to spreadsheet operations.
    """

    def update_worksheet_cell(self, worksheet, value, row, column):
        """
        Updates Google Sheet worksheet based on present month, value and column arguments.
        """
        self.clear_display()
        print(f"Updating {column} in worksheet...\n")
        month_cell = SHEET.worksheet(worksheet).find(row)
        month_income = SHEET.worksheet(worksheet).find(column)
        SHEET.worksheet(worksheet).update_cell(month_cell.row, month_income.col, value)
        print(f"{column.capitalize()} updated successfully!\n\n")

    def input_values_for_worksheet(self, worksheet, month):
        """
        Return user input for individual categories.
        """
        self.clear_display()
        self.clear_cells(worksheet, month)
        month_cell = SHEET.worksheet(worksheet).find(month)
        spendings = {}
        for item in self.categories_list:
            if item != 'TOTAL' and item!= 'SURPLUS':
                self.clear_display()
                spendings[item] = pyip.inputFloat(prompt=f"\nEnter value for {item}: \n")
            else:
                if item == 'TOTAL':
                    spendings[item] = sum(spendings.values())
                elif item == 'SURPLUS':
                    spendings[item] = self.money - spendings['TOTAL']
        self.clear_display()
        print(f"\nUpdating {worksheet} worksheet with passed values...")
        for key, value in spendings.items():
            if key != 'SURPLUS':
                key_location = SHEET.worksheet(worksheet).find(key)
                SHEET.worksheet(worksheet).update_cell(month_cell.row, key_location.col, value)
        print(f"\n{worksheet.capitalize()} worksheet updated successfully!")
        print(f"Your summarize costs for {worksheet} is: {spendings['TOTAL']}")
        
        return spendings

    def clear_cells(self, worksheet, month):
        """
        Function to clear cells for the selected month and worksheet.
        """
        self.clear_display()
        month_cell = SHEET.worksheet(worksheet).find(month)
        print(f"\nClearing {worksheet} worksheet...")
        SHEET.worksheet(worksheet).batch_clear([f"{month_cell.row}:{month_cell.row}"])
        SHEET.worksheet(worksheet).update_cell(month_cell.row, month_cell.col, month)
        print(f"\n{worksheet.capitalize()} worksheet is now clear.")


    def update_worksheet_categories(self, categories, worksheet, cell):
        """
        Updates worksheet with categories of user's choice.
        """
        self.clear_display()
        print(f"\nUpdating {worksheet} worksheet...")
        split_categories = categories.split(',')
        month = SHEET.worksheet(worksheet).find(cell)
        for num, item in enumerate(split_categories):
            if item != 'SURPLUS':
                SHEET.worksheet(worksheet).update_cell(month.row, num+2, item)
        print(f"\n{worksheet.capitalize()} worksheet updated successfully!")
        return split_categories
    
    def create_categories(self, worksheet, default_cat):
        """
        Gets user input to create peronsalized categories or use default option. Validates inputs.
        """
        flow = True
        while flow:
            self.clear_display()
            options_menu = pyip.inputMenu(['Default', 'Create Categories', 'Input values only'], prompt=f"Select how you want to manage your {worksheet.capitalize()}:\n", numbered=True)
            if options_menu == 'Create Categories':
                print("\nCreating custom categories will delete all values in the worksheet.")
                continue_bool = pyip.inputStr("Do you want to continue?\nType (Y)es or(N):\n")
                if continue_bool.lower() == 'y':
                    self.clear_display()
                    self.clear_cells(worksheet, 'Month')
                    print("\nEnter your categories WITHOUT whitespaces such as spaces or tabs and seperated with commas.")
                    print("Limit yourself to one word entries only.")
                    print("\nExample: Vehicle,Apartment,School,Bank")
                    commas = False
                    while not commas:
                        user_categories = pyip.inputStr(prompt="\nEnter your categories:\n", blockRegexes = [r'(,)\1+|^,'])
                        if user_categories.find(',') != -1 and user_categories[-1] != ',':
                            commas = True
                            flow = False
                        else:
                            print("\nYour entry is invalid! Try again.")
                else:
                    continue
            elif options_menu == 'Default':
                self.clear_cells(worksheet, 'Month')
                user_categories = default_cat
                flow = False
            else:
                all_values = SHEET.worksheet(worksheet).get_all_values()
                get_categories = all_values[0][1:]
                categories_string = ''
                for item in get_categories:
                    if item != '' and item != 'TOTAL':
                        categories_string += (item + ',')
                user_categories = var_string[:-1]
                flow = False

        return user_categories + ',TOTAL' + ',SURPLUS'


class Budget(ClearDisplayMixin, UpdateSpreadsheetMixin):
    """
    Budget class that handles user option for calculations.
    """
    def __init__(self):
        self.app_logic = self.main_menu()
        self.income = self.enter_income()
        self.plan_elements = self.choose_budget_plan()
        self.update_worksheet_cell('general', self.income[0], self.income[1], 'Monthly Income')
        
    
    def main_menu(self):
        """
        Function to display main menu.
        """
        # Concept for pyfiglet styling comes from https://www.youtube.com/watch?v=U1aUteSg2a4
        print(colored(pyfiglet.figlet_format("personal budget manager", font = "graceful", justify="center", width=110), "green"))
        
        start_sequence = False
        
        while start_sequence == False:
            show_menu = pyip.inputMenu(['About the app','Print tables', 'Manage your budget', 'Exit'], prompt="\nSelect one of the following and hit Enter:\n", numbered=True)
            if show_menu == 'About the app':
                self.clear_display()
                print("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vitae erat pellentesque, bibendum quam in, molestie augue. Integer vitae neque efficitur nunc feugiat dignissim sed non est. Pellentesque eu ullamcorper nibh. Nullam tempus lacus enim, quis vulputate mi condimentum vitae. Cras vel ullamcorper risus. Mauris nec rutrum lacus. Sed sit amet molestie lacus. Duis sit amet quam diam. Maecenas cursus risus ut magna egestas pellentesque. Curabitur dapibus maximus blandit. Nunc aliquet ante id nisl pharetra, in rhoncus neque luctus. Quisque rutrum nisi vel eros fringilla hendrerit.")

            elif show_menu == 'Print tables':
                self.clear_display()
                tables_choice = pyip.inputMenu(["general", "needs", "wants"], prompt="Select which table to print in terminal:\n", numbered=True)
                self.clear_display()
                values = SHEET.worksheet(tables_choice).get_all_values()
                table = PrettyTable()
                table.field_names = values[0]
                table.add_rows(values[1:])
                print(table)
            
            elif show_menu == "Manage your budget":
                self.clear_display()
                start_sequence = True

            else:
                quit()
        
        return start_sequence


    
    def choose_budget_plan(self):
        """
        Gets user input for budget plan based on menu presented on the screen, validates the choice, clears terinal and returns user's choice.
        """
        self.clear_display()
        while True:
            response = pyip.inputMenu(['50/30/20', '70/20/10', 'About plans'], prompt="Please select which budget plan you choose:\n", numbered=True)
            if response == '50/30/20':
                needs = round(self.income[0] * 0.5, 1)
                wants = round(self.income[0] * 0.3, 1)
                savings = round(self.income[0] * 0.2, 1)
                break
            elif response == '70/20/10':
                needs = round(self.income[0] * 0.7, 1)
                wants = round(self.income[0] * 0.2, 1)
                savings = round(self.income[0] * 0.1, 1)
                break
            else:
                self.clear_display()
                print("The 50/30/20 rule is a money management technique that divides your income into three categories:\n50% Needs(essentials)\n30% Wants(non-essentials)\n20% Savings.\n\nBy default this app provides following sub-categories:\nNeeds: Housing, Vehicle costs, Insurance, Food and Banking\nWants: Entertaintment, Wellbeing and Travel\n* Savings is what is meant to be left untouched and used only in case there is absolute need for it. It can cover any unexpected costs.\n\nThe 70/20/10 rule is less robust investment type, where the budget is split in proportion:\n70% Needs\n20% Wants\n10% Savings\n")
        return [response, needs, wants, savings]

    def enter_income(self):
        """
        Gets user's input for income, validates the choice, clears terinal and returns user's choice.
        """
        self.clear_display()
        if self.app_logic == True:
            month = pyip.inputMenu(['Present month', 'Select month'], prompt="Select which month will include calculations:\n", numbered=True)
            if month == 'Present month':
                month_calc = MONTH_NOW
            else:
                while True:
                    self.clear_display()
                    month_calc = pyip.inputStr("Type month for calculations:\n")
                    if month_calc in MONTHS:
                        break
                    else:
                        print("Incorrect input. Make sure it is capitalized name of the month.\nExample: July")
            self.clear_display()
            income = pyip.inputFloat("Enter your monthly income (-TAX): \n")
            print(month_calc)
            return income, month_calc

    def manage_your_budget(self, surplus, savings, month):
        """
        Manages SURPLUS values for selected worksheet. Transfer SURPLUS to cell selected by user.
        """
        self.clear_display()
        print("Managing budget...")
        
        all_values = SHEET.worksheet('general').get_all_records()
        month_cell = SHEET.worksheet('general').find(month)
        extra_cell = SHEET.worksheet('general').find('Extra')
        savings_cell = SHEET.worksheet('general').find('Savings')
        
        if surplus < 0:
            print("\nChecking possibles to manage your debt...")
            cover = savings + surplus
            if cover < 0:
                print("\nYou don't have enough money for your spends! You must reduce your costs!...")
                quit()
            else:
                print("\nEnough Savings to cover debt. Updating SURPLUS and Savings...")
                SHEET.worksheet('general').update_cell(month_cell.row, savings_cell.col, cover)
                print("\nSURPLUS and Savings up-to-date.")
        else:
            self.clear_display()
            add_money = pyip.inputMenu(['Savings', 'Extra Money'], prompt="Select where you want to invest your money:\n", numbered=True)
            if add_money == 'Savings':
                for dict in all_values:
                    if dict['Month'] == month:
                        SHEET.worksheet('general').update_cell(month_cell.row, savings_cell.col, dict['Savings']+surplus)
            else:
                for dict in all_values:
                    if dict['Month'] == month:
                        if dict['Extra'] == '':
                            SHEET.worksheet('general').update_cell(month_cell.row, extra_cell.col, surplus)
                        else:
                            SHEET.worksheet('general').update_cell(month_cell.row, extra_cell.col, dict['Extra']+surplus)
        print("\nBudget up-to-date!")

    
class Savings(Budget, ClearDisplayMixin):
    """
    Budget child class to handle Savings calculations.
    """
    def __init__(self, money, month):
        self.month = month
        self.money = money
        self.update_worksheet_cell('general', self.money, self.month , 'Savings')

class Needs(Budget, ClearDisplayMixin, UpdateSpreadsheetMixin):
    """
    Budget child class to handle Needs calculations.
    """
    def __init__(self, money):
        self.money = money
        self.categories_string = self.create_categories('needs', 'Housing,Vehicle,Insurance,Food,Banking')
        self.categories_list = self.update_worksheet_categories(self.categories_string, 'needs', 'Month')

class Wants(Budget, ClearDisplayMixin, UpdateSpreadsheetMixin):
    """
    Budget child class to handle Wants calculations.
    """
    def __init__(self, money):
        self.money = money
        self.categories_string = self.create_categories('wants', 'Enteraintment,Wellbeing,Travel')
        self.categories_list = self.update_worksheet_categories(self.categories_string, 'wants', 'Month')    


budget = Budget()
save = Savings(budget.plan_elements[3], budget.income[1])

needs = Needs(budget.plan_elements[1])
needs_spendings = needs.input_values_for_worksheet('needs', budget.income[1])
needs.manage_your_budget(needs_spendings['SURPLUS'], budget.plan_elements[3], budget.income[1])

wants = Wants(budget.plan_elements[2])
wants_spendings = wants.input_values_for_worksheet('wants', budget.income[1])
wants.manage_your_budget(wants_spendings['SURPLUS'], budget.plan_elements[3], budget.income[1])