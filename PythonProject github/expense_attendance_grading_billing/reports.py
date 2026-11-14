
from attendance import attendance, calculate_attendance
from grading import grades, calculate_average, get_grade
from expenses import calculate_total
from billing import bills


# Function to display one student's complete report
def student_report(roll_no):

    print("\n========== STUDENT REPORT ==========")
    print("Roll Number:", roll_no)

    # Attendance details
    if roll_no in attendance:
        percentage = calculate_attendance(roll_no)
        print("Attendance:", format(percentage, ".2f"), "%")

        if percentage >= 75:
            print("Attendance Status: Eligible")
        elif percentage >= 65:
            print("Attendance Status: Warning")
        else:
            print("Attendance Status: Shortage")
    else:
        print("Attendance: Not Available")

    # Marks details
    if roll_no in grades:
        print("Average Marks:", format(calculate_average(roll_no), ".2f"))
        print("Grade:", get_grade(roll_no))
    else:
        print("Marks: Not Available")

    # Expense details
    print("Total Expenses: Rs.", format(calculate_total(roll_no), ".2f"))

    # Billing details
    if roll_no in bills:
        print("Final Bill: Rs.", format(bills[roll_no]["final_amount"], ".2f"))
    else:
        print("Bill: Not Generated")

    print("====================================")


# Function to count attendance status
def attendance_summary():

    eligible = 0
    warning = 0
    shortage = 0

    for roll_no in attendance:

        percentage = calculate_attendance(roll_no)

        if percentage >= 75:
            eligible = eligible + 1

        elif percentage >= 65:
            warning = warning + 1

        else:
            shortage = shortage + 1

    print("\n======= ATTENDANCE SUMMARY =======")
    print("Eligible Students:", eligible)
    print("Warning Students:", warning)
    print("Shortage Students:", shortage)
    print("Total Students:", eligible + warning + shortage)
    print("=================================")

