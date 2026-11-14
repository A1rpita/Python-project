
# Manual Test Cases
## Expense Attendance Grading and Billing System

This document contains 8 manual test cases
used to test the Python CLI application.

### Test Case 1: Student Registration
Input:
- Roll Number: 101
- Name: Rahul

Expected Result:
Student should be registered successfully.

### Test Case 2: Duplicate Roll Number
Input:
- Roll Number: 101
- Name: Priya

Expected Result:
System should reject the duplicate roll number.

### Test Case 3: Empty Student Name
Input:
- Roll Number: 102
- Name: Empty

Expected Result:
System should reject an empty student name.

### Test Case 4: Negative Expense
Input:
- Roll Number: 101
- Expense Name: Books
- Amount: -100

Expected Result:
System should reject the negative expense amount.

### Test Case 5: Invalid Attendance
Input:
- Roll Number: 101
- Total Classes: 100
- Attended Classes: 120

Expected Result:
System should reject attendance greater than total classes.

### Test Case 6: Invalid Marks
Input:
- Roll Number: 101
- Marks: 85, 90, 120

Expected Result:
System should reject marks greater than 100.

### Test Case 7: Invalid Billing
Input:
- Roll Number: 101
- Extra Charges: -100

Expected Result:
System should reject negative extra charges.

### Test Case 8: Attendance Shortage
Input:
- Roll Number: 101
- Total Classes: 100
- Attended Classes: 50

Expected Result:
Attendance percentage should be 50%.
Student status should be Shortage.

---

## Conclusion

All 8 manual test cases are designed to
check valid and invalid inputs, duplicate
records, attendance calculations, grading
and billing validations.
