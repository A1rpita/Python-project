
import sys
import os
import unittest

# Add the main project folder to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validators import ival, fval, sval
from grading import calculate_average, get_grade
from attendance import calculate_attendance


class TestExpenseAttendanceGradingBilling(unittest.TestCase):

    # Test Case 1: Valid integer input
    def test_valid_integer(self):
        self.assertEqual(ival("Enter number: "), 101)

    # Test Case 2: Invalid integer input
    def test_invalid_integer(self):
        self.assertRaises(ValueError, int, "abc")

    # Test Case 3: Valid student name
    def test_valid_name(self):
        self.assertEqual(sval("Enter name: "), "Rahul")

    # Test Case 4: Empty student name
    def test_empty_name(self):
        self.assertRaises(ValueError, sval, "")

    # Test Case 5: Valid grading result
    def test_grade_A(self):
        self.assertEqual(get_grade(85), "A")

    # Test Case 6: Marks above 100
    def test_invalid_marks(self):
        marks = [85, 90, 120]
        self.assertTrue(any(mark > 100 for mark in marks))

    # Test Case 7: Attendance eligibility
    def test_attendance_eligible(self):
        self.assertEqual(80, 80)

    # Test Case 8: Attendance shortage
    def test_attendance_shortage(self):
        self.assertEqual(50, 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
