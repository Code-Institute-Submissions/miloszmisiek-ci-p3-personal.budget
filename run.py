"""
Main module to start Personal Budget Manager program.
"""

from classes.budget import Budget
from classes.elements import Needs, Wants, Savings


if __name__ == '__main__':

    # Create "budget" object.
    budget = Budget()

    # Create "save" object.
    save = Savings(budget.plan_elements[3], budget.income[1])

    # Create "needs" object and handle its calculations.
    needs = Needs(budget.plan_elements[1])
    needs_spendings = needs.input_values_for_worksheet('needs',
                                                       budget.income[1],
                                                       needs.money)
    budget.manage_your_budget('needs', needs_spendings['SURPLUS'],
                              budget.plan_elements[3], budget.income[1])

    # Create "wants" object and handle its calculations.
    wants = Wants(budget.plan_elements[2])
    wants_spendings = wants.input_values_for_worksheet('wants',
                                                       budget.income[1],
                                                       wants.money)
    budget.manage_your_budget('wants', wants_spendings['SURPLUS'],
                              budget.plan_elements[3], budget.income[1])
