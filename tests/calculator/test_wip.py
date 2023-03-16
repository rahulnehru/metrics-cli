import unittest

from src.calculator.wip import group_tickets_by_status


class TestWip(unittest.TestCase):
    tickets = [
        {
            'fields': {
                'status': {
                    'name': 'To Do'
                }
            }
        },
        {
            'fields': {
                'status': {
                    'name': 'In Progress'
                }
            }
        },
        {
            'fields': {
                'status': {
                    'name': 'In Progress'
                }
            }
        },
        {
            'fields': {
                'status': {
                    'name': 'Done'
                }
            }
        }
    ]

    def test_group_tickets_by_status_returns_correct_count_of_groupings(self):
        grouped_tickets = group_tickets_by_status(self.tickets)
        self.assertEqual(grouped_tickets['To Do'], 1)
        self.assertEqual(grouped_tickets['In Progress'], 2)
        self.assertEqual(grouped_tickets['Done'], 1)


if __name__ == '__main__':
    unittest.main()
