# Dictionary to store attendance records
attendance = {}


# Function to add student attendance

# Function to add student attendance
def add_attendance(roll_no):

    while True:
        try:
            total_classes = int(input("Enter total classes held: "))

            if total_classes <= 0:
                print("Total classes must be greater than zero.")
            else:
                break

        except ValueError:
            print("Please enter a valid whole number.")

    while True:
        try:
            attended = int(input("Enter classes attended: "))

            if attended < 0:
                print("Attendance cannot be negative.")

            elif attended > total_classes:
                print("Attended classes cannot be more than total classes.")

            else:
                break

        except ValueError:
            print("Please enter a valid whole number.")

    attendance[roll_no] = {
        "total_classes": total_classes,
        "attended": attended
    }

    print("Attendance added successfully!")



# Function to calculate attendance percentage
def calculate_attendance(roll_no):
    if roll_no not in attendance:
        return 0

    total = attendance[roll_no]["total_classes"]
    attended = attendance[roll_no]["attended"]

    percentage = (attended / total) * 100

    return percentage


# Function to check attendance eligibility
def check_attendance(roll_no):
    percentage = calculate_attendance(roll_no)

    print("\n------ ATTENDANCE REPORT ------")
    print("Roll Number:", roll_no)
    print("Attendance:", format(percentage, ".2f"), "%")

    if percentage >= 75:
        print("Status: Eligible")

    elif percentage >= 65:
        print("Status: Warning")

    else:
        print("Status: Shortage")

    return percentage
