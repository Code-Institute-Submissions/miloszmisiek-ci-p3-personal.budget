# Testing User Stories
-   As a user, I want to automate my budget calculations.
    - All calculations for budgeting can be handled using only a Python program.
-   As a user, I want to have access to my data.
    - User can print spreadsheet tables in the terminal in *Main Menu*. Values for *Needs* and *Wants* are printed and updated in the terminal every time the user makes an input for his categories.
-   As a user, I want to edit my data if needed.
    - This program allows users to enter data for previous or future months in case users would like to predict/check their budget.
-   As a user, I want to run my program without crashing.
    - Validation was automated mainly using third party libraries
-   As a user, I want to be notified if I exceeded my budget.
    - Users are not allowed to enter 'Wants' data if 'Needs' (which are ESSENTIAL) are not met. 
-   As a user, I want to handle my debt if I exceed my budget.
    - If users have done bad management of their budget, the program will check Savings and if there is enough money it will cover the debt. If the Surplus is exceeding users Savings, the message will be printed to inform them about it.

# PEP8 Validation
The program is constructed using Python technology.
Testing was completed using [PEP8 Validator](http://pep8online.com/).

All modules were tested using PEP8 Validator. Most of the bugs were related to line length (> 80 characters), trailing whitespace or too few blank lines. After validation, the final code in all modules was founded with no warnings.

![Example of PEP8 result](docs/testing-files/budget-pep8-validation.png)

The file with the first validation can be found [here](docs/testing-files/pep8-example-validation.txt).

# Code Validation
All users’ inputs are validated with a third party library [PyInputPlus](https://pypi.org/project/PyInputPlus/).
The library automates validation, so no further code structure is required.

I have manually tested the program by checking every option with valid and invalid entries through GitPod and Heroku terminals. During the code development, I was heavily relying on GitPod 'pylint' built-in feature. It checks for any pep8 errors or warnings.

# Try/Except Function
Parts of the code that require extra validation use Python built-in method *try/except*.

# Known Bugs
Most of the bugs were found using [PEP8 Validator](http://pep8online.com/) which are documented in the [PEP8 Validation](#pep8-validation) section. 

During code development, all known bugs were caught and fixed along the code structure process.

**Categories Input Validation Issue**
The first option to get users categories was to use one input entry with user categories stored as a string separated with commas. This caused a lot of issues with input validation, so it was decided to use a while loop with every category as one entry. To quit the while loop user must press 'q' and hit Enter.

**Create Categories *while loop* Issue**
The **Create Categories** method *while loop* was not breaking/continuing properly - the bug was fixed with correct indentation.

# Unsolved Bugs
## os.system('clear') not working properly in Heroku.
This program uses heavily the *os.system('clear')* function to remove content from the terminal. During Heroku deployment, it was noticed, that the Heroku console is not clearing as expected: the top part of the console is overlapping with the new content. The decision was made to restrict content to 24 lines (Heroku console height) and when it is not possible (*Print tables* option in *Main Menu*) - remove the title logo.

The problem will be still present during input validation - too many users mistakes will cause the text to accumulate and the *clear* method will not properly remove the content when it exceeds 24 lines in height.