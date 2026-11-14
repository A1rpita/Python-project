
# Dictionary to store student marks
grades = {}




# Function to add student marks
def add_marks(roll_no):

    while True:
        try:
            marks = input("Enter marks separated by commas: ").strip()

            if marks == "":
                print("Please enter marks.")
                continue

            mark_list = list(map(float, marks.split(",")))

            valid = True

            for mark in mark_list:
                if mark < 0 or mark > 100:
                    valid = False
                    break

            if valid:
                grades[roll_no] = mark_list
                print("Marks added successfully!")
                break

            else:
                print("Marks should be between 0 and 100.")

        except ValueError:
            print("Please enter valid numbers.")




# Function to calculate total marks
def calculate_total(roll_no):

    if roll_no not in grades:
        return 0

    total = 0

    for mark in grades[roll_no]:
        total = total + mark

    return total


# Function to calculate average marks
def calculate_average(roll_no):

    if roll_no not in grades:
        return 0

    total = calculate_total(roll_no)
    count = len(grades[roll_no])

    return total / count


# Function to assign grade
def get_grade(roll_no):

    if roll_no not in grades:
        return "No Result"

    average = calculate_average(roll_no)

    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "Fail"


# Function to display student result
def view_result(roll_no):

    if roll_no not in grades:
        print("No marks found for this student.")
        return

    print("\n------ STUDENT RESULT ------")
    print("Roll Number:", roll_no)
    print("Total Marks:", format(calculate_total(roll_no), ".2f"))
    print("Average Marks:", format(calculate_average(roll_no), ".2f"))
    print("Grade:", get_grade(roll_no))
