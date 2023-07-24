import unittest
import datetime

from src.calculator.cycletime import get_creation_date, get_resolution_date, get_cycle_time, \
    calculate_ave_cycletime, calculate_percentile_cycle_time

from src.config.config import Config


class TestCycletime(unittest.TestCase):
    def test_get_creation_date_returns_value_from_ticket(self):
        ticket = {'fields': {'created': '2018-01-01T00:00:00.000+0000'}}
        actual = get_creation_date(ticket)
        expected = datetime.datetime.strptime('2018-01-01T00:00:00.000+0000', "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(actual, expected)

    def test_get_creation_date_raises_value_error_when_ticket_has_no_created_field(self):
        ticket = {'fields': {}}
        self.assertRaises(ValueError, get_creation_date, ticket)

    def test_get_creation_date_raises_value_error_when_incorrect_format(self):
        ticket = {'fields': {'created': '2018-01-01'}}
        self.assertRaises(ValueError, get_creation_date, ticket)

    def test__get_resolution_date_returns_value_from_ticket_when_ticket_has_resolution_date(self):
        ticket = {'fields': {'resolutiondate': '2018-01-01T00:00:00.000+0000'}}
        resolved_status = []
        actual = get_resolution_date(resolved_status, ticket)
        expected = datetime.datetime.strptime('2018-01-01T00:00:00.000+0000', "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(actual, expected)

    def test__get_resolution_date_returns_value_from_ticket_when_ticket_no_resolution_date(self):
        ticket = {'fields': {'resolutiondate': None},
                  'changelog': {
                      'histories': [
                          {
                              'created': '2018-01-01T00:00:00.000+0000',
                              'items': [
                                  {
                                      'field': 'status',
                                      'toString': 'Done'
                                  }
                              ]
                          }
                      ]
                  }
                  }
        resolved_status = ['Done']
        actual = get_resolution_date(resolved_status, ticket)
        expected = datetime.datetime.strptime('2018-01-01T00:00:00.000+0000', "%Y-%m-%dT%H:%M:%S.%f%z")
        self.assertEqual(actual, expected)

    def test__get_resolution_date_raises_value_error_when_ticket_has_no_resolution_date_and_not_completed(self):
        ticket = {
            'key': 'TEST-1',
            'fields': {'resolutiondate': None},
            'changelog': {
                'histories': [
                    {
                        'created': '2018-01-01T00:00:00.000+0000',
                        'items': [
                            {
                                'field': 'status',
                                'toString': 'In Progress'
                            }
                        ]
                    }
                ]
            }
        }
        resolved_status = ['Done']
        self.assertRaises(Warning, get_resolution_date, resolved_status, ticket)

    def test_get_cycle_time_returns_correct_number_of_days_for_ticket_with_resolution_date(self):
        resolved_statuses = ['Done']
        ticket = {
            'key': 'TEST-1',
            'fields': {
                'resolutiondate': '2018-01-04T00:00:00.000+0000',
                'created': '2018-01-01T00:00:00.000+0000'
            }
        }
        actual = get_cycle_time(resolved_statuses, ticket)
        expected = 3
        self.assertEqual(actual, expected)

    def test_get_cycle_time_returns_correct_number_of_days_for_ticket_with_no_resolution_date(self):
        resolved_statuses = ['Done']
        ticket = {
            'key': 'TEST-1',
            'fields': {
                'resolutiondate': None,
                'created': '2018-01-01T00:00:00.000+0000'
            },
            'changelog': {
                'histories': [
                    {
                        'created': '2018-01-04T00:00:00.000+0000',
                        'items': [
                            {
                                'field': 'status',
                                'toString': 'Done'
                            }
                        ]
                    }
                ]
            }
        }
        actual = get_cycle_time(resolved_statuses, ticket)
        expected = 3
        self.assertEqual(actual, expected)

    def test_calculate_average_cycle_time_returns_average_cycletime_of_all_tickets(self):
        tickets = [
            {
                'key': 'TEST-1',
                'fields': {
                    'resolutiondate': '2018-01-03T00:00:00.000+0000',
                    'created': '2018-01-01T00:00:00.000+0000'
                }
            },
            {
                'key': 'TEST-2',
                'fields': {
                    'resolutiondate': '2018-01-03T00:00:00.000+0000',
                    'created': '2018-01-01T00:00:00.000+0000'
                }
            },
            {
                'key': 'TEST-3',
                'fields': {
                    'resolutiondate': '2018-01-09T00:00:00.000+0000',
                    'created': '2018-01-01T00:00:00.000+0000'
                }
            }
        ]
        resolved_statuses = ['Done']

        config = Config(config_file='tests/resources/test_config.yaml', weeks=3)
        actual = calculate_ave_cycletime(config, tickets)
        expected = 4
        self.assertEqual(actual, expected)

    def test_calculate_average_cycle_time_raises_warning_when_tickets_length_is_zero(self):
        config = Config(config_file='tests/resources/test_config.yaml', weeks=3)
        self.assertRaises(Warning, calculate_ave_cycletime, config, [])

    def test_calculate_percentile_cycle_time_returns_correct_percentile(self):
        tickets = [
            {
                'key': 'TEST-1',
                'fields': {
                    'resolutiondate': '2018-01-03T00:00:00.000+0000',
                    'created': '2018-01-01T00:00:00.000+0000'
                }
            },
            {
                'key': 'TEST-2',
                'fields': {
                    'resolutiondate': '2018-01-03T00:00:00.000+0000',
                    'created': '2018-01-01T00:00:00.000+0000'
                }
            },
            {
                'key': 'TEST-3',
                'fields': {
                    'resolutiondate': '2018-01-09T00:00:00.000+0000',
                    'created': '2018-01-01T00:00:00.000+0000'
                }
            }
        ]
        resolved_statuses = ['Done']
        self.assertEqual(calculate_percentile_cycle_time(resolved_statuses, tickets, 0.5), 2)
        self.assertEqual(calculate_percentile_cycle_time(resolved_statuses, tickets, 0.75), 8)
        self.assertEqual(calculate_percentile_cycle_time(resolved_statuses, tickets, 0.85), 8)


if __name__ == '__main__':
    unittest.main()
