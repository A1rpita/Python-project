
from validators import sval, fval

# Dictionary to store student expenses
expenses = {}




# Function to add an expense
def add_expense(roll_no):

    name = sval("Enter expense name: ")

    while True:
        try:
            amount = float(input("Enter expense amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                break

        except ValueError:
            print("Please enter a valid amount.")

    if roll_no not in expenses:
        expenses[roll_no] = []

    expense = {
        "name": name,
        "amount": amount
    }

    expenses[roll_no].append(expense)

    print("Expense added successfully!")



# Function to display expenses
def view_expenses(roll_no):

    if roll_no not in expenses or len(expenses[roll_no]) == 0:
        print("No expenses found for this student.")
        return

    print("\n------ STUDENT EXPENSES ------")

    total = 0

    for expense in expenses[roll_no]:
        print("Expense:", expense["name"])
        print("Amount: Rs.", format(expense["amount"], ".2f"))

        total = total + expense["amount"]

    print("------------------------------")
    print("Total Expense: Rs.", format(total, ".2f"))


# Function to calculate total expenses
def calculate_total(roll_no):

    total = 0

    if roll_no in expenses:
        for expense in expenses[roll_no]:
            total = total + expense["amount"]

    return total
