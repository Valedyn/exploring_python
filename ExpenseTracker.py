# imports
import os
from enum import Enum
import json
import tempfile
import shutil


# enum for expense types
class ExpenseType(Enum):
    RENT = 1
    GROCERIES = 2
    TRANSPORTATION = 3
    ENTERTAINMENT = 4


# expense class with definitions
class Expense:
    def __init__(self, name, cost, date, expense_type):
        self.name = name
        self.cost = float(cost)
        self.date = date
        self.expense_type = expense_type


# class for handling expenses, as well as handling basic data saving (no databank, this isn't complex enough)
class ExpenseJSONHandler:
    # _instance for singleton
    _instance = None
    # os-independent path
    json_file_path = os.path.join(tempfile.gettempdir(), "ExpenseTracker", "expenses.json")

    # method ran when creating a new instance
    def __new__(cls, *args, **kwargs):
        # checks if the _instance variable isn't set
        if cls._instance is None:
            # runs the object constructor, creating a new instance of this object without using *this* specific method
            cls._instance = super().__new__(cls)
        return cls._instance

    # default constructor
    def __init__(self):
        # checks whether the directory of the expenses.json file exists (ExpenseTracker)
        if not os.path.exists(os.path.dirname(self.json_file_path)):
            # creates it if not
            os.makedirs(os.path.dirname(self.json_file_path))

        # checks whether the json file that is used as a pseudo database exists
        if not os.path.exists(self.json_file_path):
            # creates an empty json file if not
            with open(self.json_file_path, "w") as f:
                f.write(json.dumps({}))
        # otherwise it reads it
        with open(self.json_file_path, "r") as f:
            file_content = f.read().strip()

            # creates dictionary
            if not file_content:
                self.expenseJSON = {}
            else:
                self.expenseJSON = json.loads(file_content)

    pass

    # adds an expense to the json file, then updates that file to reflect the changes
    def add_to_list(self, expense):
        # checks whether the expense type is in the json file
        if expense.expense_type.name not in self.expenseJSON:
            # if not, it creates an empty array for that type
            self.expenseJSON[expense.expense_type.name] = []

        # adds an expense to the category
        self.expenseJSON[expense.expense_type.name].append({
            "name": expense.name,
            "cost": expense.cost,
            "date": expense.date
        })

        # update
        self.update_file()

    def remove_from_list(self, expense_type, expense_name):
        # check to see whether expense_type even exists
        if expense_type.name in self.expenseJSON:
            counter = 0
            # loop to find expense with expense_name
            for dict_value in self.expenseJSON[expense_type.name]:
                # if expense_name exists
                if expense_name == dict_value["name"]:
                    # deletes json element
                    del self.expenseJSON[expense_type.name][counter]

                    # updates json
                    self.update_file()
                    return True
                counter += 1

        return False

    def update_file(self):
        # updates json file
        with open(self.json_file_path, "w") as f:
            f.write(json.dumps(self.expenseJSON, indent=4))

    # reads json file
    def read_file(self):
        with open(self.json_file_path, "r") as f:
            print(f.read())


# deletes all files
def delete_expense_files():
    # os-independent path
    path = os.path.join(tempfile.gettempdir(), "ExpenseTracker")
    if os.path.exists(path):
        # removes the directory and files
        shutil.rmtree(os.path.join(tempfile.gettempdir(), "ExpenseTracker"))


# example code

# t = ExpenseJSONHandler()
# expense = Expense("streaming service", 3.40, "2024-10-13", ExpenseType.ENTERTAINMENT)
# t.add_to_list(expense_thing)
# t.remove_from_list(ExpenseType.ENTERTAINMENT, "streaming service")
# t.update_file()
