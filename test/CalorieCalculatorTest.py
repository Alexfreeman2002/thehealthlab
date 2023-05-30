import unittest
from CalorieCounter.calc_cals import calculate_calories

class TestCalories(unittest.TestCase):
    def test_calculate_calories(self):

        # define test data and run the function
        calories = calculate_calories(protein=130, fat=60, carbs=300)

        # expected result
        expected = 2260

        # tests whether the expected result is equal to the actual result
        self.assertEqual(expected, calories)


if __name__ == '__main__':
    unittest.main()