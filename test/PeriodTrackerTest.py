import unittest
from datetime import datetime, timedelta
from app import db
from models import Period
from PeriodTracker.forms import PeriodForm
from PeriodTracker.views import calculate_next_period


# Create the class of Period Tracker testing file for unit test
class TestPeriodTracker(unittest.TestCase):
    # Define the test function of period tracker
    def test_calculate_next_period(self):
        # Define the testing data of the current period information
        start_date = datetime(2023, 3, 27)
        end_date = datetime(2023, 4, 3)
        period_duration = 8
        period_cycle = 28

        # Call the calculate function to get the calculated results
        next_start_date, next_end_date, ovulation = calculate_next_period(start_date, end_date, period_duration,
                                                                          period_cycle)

        # Define the testing data of the next period information
        expected_next_start_date = datetime(2023, 4, 24)
        expected_next_end_date = datetime(2023, 5, 1)
        expected_ovulation = datetime(2023, 4, 10)

        # Test whether the results from the calculate function is equal to the testing data of the next period information
        self.assertEqual(next_start_date, expected_next_start_date)
        self.assertEqual(next_end_date, expected_next_end_date)
        self.assertEqual(ovulation, expected_ovulation)


if __name__ == '__main__':
    unittest.main()
