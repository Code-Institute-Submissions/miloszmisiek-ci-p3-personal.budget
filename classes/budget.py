import time
import os
import sys
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip

from prettytable import PrettyTable

from classes.systemmixin import SystemMixin
from classes.updatespreadsheetmixin import UpdateSpreadsheetMixin

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
MONTHS = ['January', 'February', 'March', 'April',
          'May', 'June', 'July', 'August', 'September',
          'October', 'November', 'December']


class Budget(SystemMixin, UpdateSpreadsheetMixin):
    """
    Budget class that handles user option for calculations.
    """
    def __init__(self):
        self.app_logic = self.main_menu()
        self.income = self.enter_income()
        self.plan_elements = self.choose_budget_plan()

    def main_menu(self):
        """
        Method to display main menu.
        """
        self.clear_display()
        start_sequence = False

        while not start_sequence:
            show_menu = pyip.inputMenu(['About the app', 'Print tables',
                                        'Manage your budget', 'Exit'],
                                       prompt="Select one of the following"
                                              "and hit Enter:\n",
                                       numbered=True)
            if show_menu == 'About the app':
                self.clear_display()
                print("This app is designed to control your monthly costs."
                      "\nWith this program you will be able to:"
                      "\n- Enter your income or get income from spreadsheet,"
                      "\n- Choose investing plan from two available,"
                      "\n- Create your own groups for costs "
                      "which will be included"
                      "\n  in Needs or Wants worksheets,"
                      "\n- Enter your costs and receive information "
                      "how much you is left"
                      "\n- If you exceed your limit, the program "
                      "will check if the debt can be covered,"
                      "\n  if not you will be prompt to restart "
                      "program and enter inputs again.")

            elif show_menu == 'Print tables':
                self.clear_display()
                tables_choice = pyip.inputMenu(["general", "needs", "wants"],
                                               prompt="Select which table "
                                               "to print in terminal:\n",
                                               numbered=True)
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
                sys.exit(0)

        return start_sequence

    def choose_month(self):
        """
        Returns month for calulations based on user input.
        """
        month = pyip.inputMenu(['Present month', 'Select month',
                                'Back to Main Menu'],
                               prompt="Select which month will "
                               "include calculations:\n",
                               numbered=True)
        if month == 'Present month':
            month_calc = MONTH_NOW
        elif month == 'Select month':
            while True:
                self.clear_display()
                month_calc = pyip.inputStr(
                    "Type month for calculations:\n").capitalize()
                if month_calc.capitalize() in MONTHS:
                    break
                print("Incorrect input. Make sure your input "
                      "is a name of the month.\nExample: July")
                time.sleep(5)
        else:
            os.execl(sys.executable, sys.executable, *sys.argv)
        self.clear_display()

        return month_calc

    def enter_income(self):
        """
        Gets user's input for income,
        validates the choice returns user's choice.
        """
        self.clear_display()
        all_values = SHEET.worksheet('general').get_all_records()
        month_calc = self.choose_month()

        while True:
            input_decision = pyip.inputMenu(['Enter monthly income',
                                             'Get income from spreadsheet',
                                             'Back to Main Menu'],
                                            prompt="Select income "
                                                   "for calculations:\n",
                                            numbered=True)
            if input_decision == 'Enter monthly income':
                self.clear_display()
                income = pyip.inputFloat("Enter your monthly "
                                         "income (-TAX): \n")
                self.update_worksheet_cell('general', income,
                                           month_calc, 'Monthly Income')
                break
            if input_decision == 'Get income from spreadsheet':
                # bug to fix - spreadsheet wrong month or monthly income wrong naming
                try:
                    for dic in all_values:
                        if dic['Month'] == month_calc and \
                           dic['Monthly Income'] != '':
                            income = dic['Monthly Income']
                        elif (dic['Month'] == month_calc and
                              dic['Monthly Income'] == ''):
                            raise ValueError()
                    break
                except ValueError:
                    print("Something went wrong. Check if name of columns "
                          "and rows in spreadsheet are correct and if "
                          "Monthly Income is not empty.\n")
                    continue
            else:
                os.execl(sys.executable, sys.executable, *sys.argv)

        return income, month_calc

    def choose_budget_plan(self):
        """
        Gets user input for budget plan based on menu presented on the screen,
        validates the choice and returns user's choice.
        """
        self.clear_display()
        while True:
            response = pyip.inputMenu(['About plans', '50/30/20', '70/20/10',
                                       'Back to Main Menu'],
                                      prompt="Please select which budget plan "
                                             "you choose:\n",
                                      numbered=True)
            if response == 'Back to Main Menu':
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                try:
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
                    elif response == 'About plans':
                        self.clear_display()
                        print("The 50/30/20 rule is a money management "
                              "technique that divides your income into "
                              "three categories:"
                              "\n50% Needs(essentials)"
                              "\n30% Wants(non-essentials)"
                              "\n20% Savings."
                              "\n\nBy default this app provides "
                              "following sub-categories:"
                              "\nNeeds: Housing, Vehicle costs, Insurance, "
                              "Food and Banking"
                              "\nWants: Entertainment, Wellbeing and Travel"
                              "\n* Savings is what is meant to be left "
                              "untouched and used only "
                              "in case there is\nabsolute need for it. "
                              "It can cover any unexpected costs."
                              "\n\nThe 70/20/10 rule is less robust "
                              "investment type, where the budget is "
                              "split in\nproportion:"
                              "\n70% Needs\n20% Wants\n10% Savings\n")
                except: # pylint: disable=bare-except
                    print("Something went wrong. "
                          "Check your income value in spreadsheet "
                          "or enter income manually.")
                    self.restart_program()
        return [response, needs, wants, savings]

    def manage_your_budget(self, worksheet, surplus, savings, month):
        """
        Manages SURPLUS values for selected worksheet.
        Transfer SURPLUS to cell selected by user.
        """
        self.clear_display()
        print("Managing budget...\n")
        time.sleep(3)

        month_cell = SHEET.worksheet('general').find(month)
        savings_cell = SHEET.worksheet('general').find('Savings')

        if surplus < 0:
            self.clear_display()
            print(f"Your Surplus for {self.color_worksheet_names(worksheet)} "
                  f"is {surplus}\n")
            print("\nChecking possibles to manage your debt...")
            time.sleep(3)
            cover = savings + surplus
            if cover < 0:
                print("\nYou don't have enough money for your spends! "
                      "You must reduce your costs!...")
                self.restart_program()
            else:
                print("\nEnough Savings to cover debt. "
                      "Updating SURPLUS and Savings...")
                time.sleep(3)
                SHEET.worksheet('general').update_cell(month_cell.row,
                                                       savings_cell.col, cover)
                print("\nSURPLUS and Savings up-to-date.")
                time.sleep(3)
        else:
            self.clear_display()
            print(f"Your Surplus for {self.color_worksheet_names(worksheet)} "
                  f"is {surplus}\n")
            self.invset_money(month, month_cell, savings_cell, surplus)

        print("\nBudget up-to-date!")
        if worksheet == 'wants':
            self.restart_program()

    def invset_money(self, month, month_cell, savings_cell, surplus):
        """
        Updates Savings or Extra in spreadsheet depending on user input.
        """
        all_values = SHEET.worksheet('general').get_all_records()
        extra_cell = SHEET.worksheet('general').find('Extra')

        add_money = pyip.inputMenu(['Savings', 'Extra Money',
                                    'Back to Main Menu'],
                                   prompt="Select where to "
                                          "invest your money:\n",
                                   numbered=True)
        if add_money == 'Savings':
            self.clear_display()
            print("Updating Savings value...\n")
            time.sleep(3)
            for dic in all_values:
                if dic['Month'] == month:
                    SHEET.worksheet('general').update_cell(
                                                            month_cell.row,
                                                            savings_cell.col,
                                                            dic['Savings'] +
                                                            surplus
                                                            )
            print("Savings value up-to date!\n")
            time.sleep(3)
        elif add_money == 'Extra Money':
            self.clear_display()
            print("Updating Extra value...\n")
            time.sleep(3)
            for dic in all_values:
                if dic['Month'] == month:
                    if dic['Extra'] == '':
                        SHEET.worksheet('general').update_cell(
                            month_cell.row, extra_cell.col, surplus)
                    else:
                        SHEET.worksheet('general').update_cell(
                            month_cell.row, extra_cell.col,
                            dic['Extra']+surplus)
            print("Extra value up-to-date!")
            time.sleep(3)
        else:
            os.execl(sys.executable, sys.executable, *sys.argv)
