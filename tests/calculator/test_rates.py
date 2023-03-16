import unittest

from src.calculator.rates import _get_number_of_working_days_in_past_weeks, _calculate_rate
from src.config.config import Config
import datetime


class TestRates(unittest.TestCase):

    config = Config(config_file='tests/resources/test_config.yaml', weeks=3)

    def test_get_number_of_working_days_in_past_weeks(self):
        from_date = datetime.datetime.now() - datetime.timedelta(weeks=3)
        number_of_working_days = 0
        while from_date < datetime.datetime.now():
            if from_date.weekday() < 5:
                number_of_working_days += 1
            from_date += datetime.timedelta(days=1)
        actual = _get_number_of_working_days_in_past_weeks(self.config)
        self.assertEqual(actual, number_of_working_days)

    def test_calculate_rate_returns_correct_value(self):
        actual = _calculate_rate(10, 5)
        self.assertEqual(actual, 2)

    def test_calculate_rate_raises_value_error_when_number_of_working_days_is_zero(self):
        self.assertRaises(ValueError, _calculate_rate, 10, 0)


if __name__ == '__main__':
    unittest.main()
