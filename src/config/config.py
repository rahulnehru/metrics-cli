import yaml
from .project import Project


def _map_to_projects(projects_dict) -> list[Project]:
    projects = []
    for project in projects_dict:
        projects.append(Project(project['team'], project['jql']))
    return projects


def _get_statuses_as_string(statuses: list[str]) -> str:
    return f'({",".join(statuses)})'


class Config:
    jira_url: str
    resolved_statuses: list[str]
    backlog_statuses: list[str]
    discarded_statuses: list[str]
    projects: list[Project]
    weeks: int
    debug_enabled: bool
    cycletime_percentiles: list[float]

    def __init__(self, config_file: str, weeks: int | None) -> None:
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.jira_url = config['jira']['url']
            self.resolved_statuses = config['jira']['statuses']['resolved']
            self.backlog_statuses = config['jira']['statuses']['backlog']
            self.discarded_statuses = config['jira']['statuses']['discarded']
            self.projects = _map_to_projects(config['projects'])
            self.debug_enabled = config['debug_enabled']
            self.weeks = weeks
            self.cycletime_percentiles = config['cycletime_percentiles']

    def get_resolved_statuses_as_string(self) -> str:
        return _get_statuses_as_string(self.resolved_statuses)

    def get_backlog_statuses_as_string(self) -> str:
        return _get_statuses_as_string(self.backlog_statuses)

    def get_discarded_statuses_as_string(self) -> str:
        return _get_statuses_as_string(self.discarded_statuses)

    def __str__(self):
        return f'Jira URL: {self.jira_url}\n' \
               f'Resolved statuses: {self.resolved_statuses}\n' \
               f'Backlog statuses: {self.backlog_statuses}\n' \
               f'Discarded statuses: {self.discarded_statuses}\n' \
               f'Projects: {self.projects}\n' \
               f'Weeks: {self.weeks}\n' \
               f'Debug enabled: {self.debug_enabled}\n' \
               f'Cycletime percentiles: {self.cycletime_percentiles}'

    @staticmethod
    def get_yaml_template() -> str:
        config = {
            'jira': {
                'url': 'https://jira.example.com',
                'statuses': {
                    'resolved': ['Done', 'Closed'],
                    'backlog': ['Backlog'],
                    'discarded': ['Discarded']
                }
            },
            'projects': [
                {
                    'team': 'Team 1',
                    'jql': 'project = PROJ1'
                }
            ],
            'debug_enabled': False,
            'cycletime_percentiles': [0.5, 0.75, 0.85, 0.95]
        }
        return config
