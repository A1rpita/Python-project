
from validators import ival, sval
from expenses import add_expense, view_expenses
from attendance import add_attendance, check_attendance
from grading import add_marks, view_result
from billing import generate_bill, view_bill
from reports import student_report, attendance_summary


# Dictionary to store student details
students = {}


# Function to register a student
def register_student():

    print("\n------ STUDENT REGISTRATION ------")

    roll_no = sval("Enter student roll number: ")

    if roll_no in students:
        print("This roll number is already registered.")
        return

    name = sval("Enter student name: ")

    students[roll_no] = {
        "name": name
    }

    print("Student registered successfully!")


# Function to check student registration
def check_student():

    roll_no = sval("Enter student roll number: ")

    if roll_no not in students:
        print("Student not found. Please register first.")
        return None

    print("Student Name:", students[roll_no]["name"])

    return roll_no


# Main menu function
def main():

    while True:

        print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
        print("1. Register Student")
        print("2. Add Student Expenses")
        print("3. View Student Expenses")
        print("4. Add Student Attendance")
        print("5. Check Attendance")
        print("6. Add Student Marks")
        print("7. View Student Result")
        print("8. Generate Student Bill")
        print("9. View Complete Student Report")
        print("10. Attendance Summary")
        print("11. Exit")
        print("================================================")

        choice = ival("Enter your choice: ", 1, 11)

        if choice == 1:

            register_student()

        elif choice == 2:

            roll_no = check_student()

            if roll_no is not None:
                add_expense(roll_no)

        elif choice == 3:

            roll_no = check_student()

            if roll_no is not None:
                view_expenses(roll_no)

        elif choice == 4:

            roll_no = check_student()

            if roll_no is not None:
                add_attendance(roll_no)

        elif choice == 5:

            roll_no = check_student()

            if roll_no is not None:
                check_attendance(roll_no)

        elif choice == 6:

            roll_no = check_student()

            if roll_no is not None:
                add_marks(roll_no)

        elif choice == 7:

            roll_no = check_student()

            if roll_no is not None:
                view_result(roll_no)

        elif choice == 8:

            roll_no = check_student()

            if roll_no is not None:
                generate_bill(roll_no)

        elif choice == 9:

            roll_no = check_student()

            if roll_no is not None:
                student_report(roll_no)

        elif choice == 10:

            attendance_summary()

        elif choice == 11:

            print("\nThank you for using Student Management System!")
            print("Program closed successfully.")
            break


# Start the program
if __name__ == "__main__":
    main()
