import unittest

from src.calculator.wastage import _calculate_wastage


class TestWastage(unittest.TestCase):

    def test_calculate_wastage_should_return_zero_when_no_wastage(self):
        discarded_tickets = []
        completed_tickets = [{'key': 'ABC-123'}]
        wastage = _calculate_wastage(completed_tickets, discarded_tickets)
        self.assertEqual(wastage, 0)

    def test_calculate_wastage_should_return_100_when_all_tickets_are_wasted(self):
        discarded_tickets = [{'key': 'ABC-123'}]
        completed_tickets = []
        wastage = _calculate_wastage(completed_tickets, discarded_tickets)
        self.assertEqual(wastage, 100)

    def test_calculate_wastage_should_return_correct_wastage_rate(self):
        discarded_tickets = [{'key': 'ABC-123'}, {'key': 'ABC-124'}]
        completed_tickets = [{'key': 'ABC-125'}, {'key': 'ABC-126'}]
        wastage = _calculate_wastage(completed_tickets, discarded_tickets)
        self.assertEqual(wastage, 50)

    def test_calculate_wastage_should_raise_error_when_no_completed_tickets(self):
        discarded_tickets = []
        completed_tickets = []
        self.assertRaises(ValueError, _calculate_wastage, completed_tickets, discarded_tickets)


if __name__ == '__main__':
    unittest.main()
