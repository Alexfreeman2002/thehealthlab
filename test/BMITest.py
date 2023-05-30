from BMI.calc_bmi import bmi_calc
import unittest


class TestBMI(unittest.TestCase):
    def test_calculate_bmi(self):
        #define test data and run the function
        bmi = bmi_calc(height=170, weight=85, h_choice="cm", w_choice="kg")

        #expected result
        expected_bmi = 29.41

        #tests whether the expected result is equal to the actual result
        self.assertEqual(expected_bmi, bmi)


if __name__ == '__main__':
    unittest.main()