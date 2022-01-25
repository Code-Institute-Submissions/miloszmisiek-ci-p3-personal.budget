import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('personal-budget')


class Budget:
    def __init__(self, plan, income, currency):
        self.plan = plan
        self.income = income
        self.currency = currency
    

class Savings(Budget):

    def calculate_savings(self):
        if self.plan == "50/30/20":
            return self.income * 0.2
        elif self.plan == "70/20/10":
            return self.income * 0.1
        else:
            raise TypeError("Incorrect type for plan argument")


save = Savings("50/30/20", 3000)
calc_save = save.calculate_savings()
print(calc_save)