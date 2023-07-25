import unittest

from src.config.config import Config


class TestConfig(unittest.TestCase):
    config = Config(config_file='tests/resources/test_config.yaml', weeks=3)

    def test_init_loads_config_file(self):
        self.assertEqual(self.config.jira_url, 'https://jira.com/rest/api/2/search')
        self.assertEqual(self.config.resolved_statuses, ['Done'])
        self.assertEqual(self.config.backlog_statuses, ['Backlog', 'New'])
        self.assertEqual(self.config.discarded_statuses, ['Closed'])
        self.assertEqual(self.config.debug_enabled, False)
        self.assertEqual(self.config.weeks, 3)
        self.assertEqual(len(self.config.projects), 2)

    def test_map_to_projects_returns_correct_projects(self):
        self.assertEqual(self.config.projects[0].team, 'Team 1')
        self.assertEqual(self.config.projects[0].jql, 'project = PROJ1 and assignedTeam = "Team 1"')
        self.assertEqual(self.config.projects[1].team, 'Team 2')
        self.assertEqual(self.config.projects[1].jql, 'project = PROJ2 and assignedTeam = "Team 2"')

    def test_get_resolved_statuses_as_string_returns_correct_string(self):
        actual = self.config.get_resolved_statuses_as_string()
        self.assertEqual(actual, '(Done)')

    def test_get_backlog_statuses_as_string_returns_correct_string(self):
        actual = self.config.get_backlog_statuses_as_string()
        self.assertEqual(actual, '(Backlog,New)')

    def test_get_discarded_statuses_as_string_returns_correct_string(self):
        actual = self.config.get_discarded_statuses_as_string()
        self.assertEqual(actual, '(Closed)')


if __name__ == '__main__':
    unittest.main()
