
from expenses import calculate_total

# Dictionary to store student bills
bills = {}



# Function to generate student bill
def generate_bill(roll_no):

    print("\n------ STUDENT BILLING ------")

    expense_amount = calculate_total(roll_no)

    print("Total Expenses: Rs.", format(expense_amount, ".2f"))

    # Taking extra charges
    while True:
        try:
            extra_charges = float(input("Enter extra charges: "))

            if extra_charges < 0:
                print("Charges cannot be negative.")
            else:
                break

        except ValueError:
            print("Please enter a valid amount.")

    total_amount = expense_amount + extra_charges

    # Taking discount
    while True:
        try:
            discount = float(input("Enter discount amount: "))

            if discount < 0:
                print("Discount cannot be negative.")

            elif discount > total_amount:
                print("Discount cannot exceed the total bill.")

            else:
                break

        except ValueError:
            print("Please enter a valid amount.")

    final_amount = total_amount - discount

    bills[roll_no] = {
        "expenses": expense_amount,
        "extra_charges": extra_charges,
        "discount": discount,
        "final_amount": final_amount
    }

    print("\n------ FINAL BILL ------")
    print("Roll Number:", roll_no)
    print("Expenses: Rs.", format(expense_amount, ".2f"))
    print("Extra Charges: Rs.", format(extra_charges, ".2f"))
    print("Discount: Rs.", format(discount, ".2f"))
    print("Final Amount: Rs.", format(final_amount, ".2f"))

    print("-----------------------")
    print("Bill generated successfully!")



# Function to view student bill
def view_bill(roll_no):

    if roll_no not in bills:
        print("No bill found for this student.")
        return

    bill = bills[roll_no]

    print("\n------ BILL DETAILS ------")
    print("Roll Number:", roll_no)
    print("Expenses: Rs.", format(bill["expenses"], ".2f"))
    print("Extra Charges: Rs.", format(bill["extra_charges"], ".2f"))
    print("Discount: Rs.", format(bill["discount"], ".2f"))
    print("Final Amount: Rs.", format(bill["final_amount"], ".2f"))
