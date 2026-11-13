# Function to take integer input
def ival(message, minimum=None, maximum=None):
    while True:
        try:
            number = int(input(message))

            if minimum is not None and number < minimum:
                print("Number is too small. Try again.")
            elif maximum is not None and number > maximum:
                print("Number is too large. Try again.")
            else:
                return number

        except ValueError:
            print("Please enter a valid whole number.")


# Function to take decimal input
def fval(message):
    while True:
        try:
            number = float(input(message))

            if number < 0:
                print("Please enter a positive amount.")
            else:
                return number

        except ValueError:
            print("Please enter a valid number.")


# Function to take text input
def sval(message):
    while True:
        value = input(message).strip()

        if value == "":
            print("This field cannot be empty.")
        else:
            return value


# Function to enter marks of different subjects
def read_marks():
    while True:
        try:
            marks = list(map(float, input(
                "Enter subject marks separated by spaces: "
            ).split()))

            if len(marks) == 0:
                print("Please enter marks.")
            else:
                valid = True

                for mark in marks:
                    if mark < 0 or mark > 100:
                        valid = False

                if valid:
                    return marks
                else:
                    print("Marks should be between 0 and 100.")

        except ValueError:
            print("Please enter numbers only.")
