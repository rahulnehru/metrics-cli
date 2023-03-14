import yaml
from .project import Project

class Config:
    jira_url: str
    resolved_statuses: list[str]
    backlog_statuses: list[str]
    discarded_statuses: list[str]
    projects: list[Project]
    weeks: int

    def __init__(self, config_file: str, weeks: int) -> None:
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.jira_url = config['jira']['url']
            self.resolved_statuses = config['jira']['statuses']['resolved']
            self.backlog_statuses = config['jira']['statuses']['backlog']
            self.discarded_statuses = config['jira']['statuses']['discarded']
            self.projects = self._map_to_projects(config['projects'])
            self.debug_enabled = config['debug_enabled']
            self.weeks = weeks

    def _map_to_projects(self, projects_dict) -> list[Project]:
        projects = []
        for project in projects_dict:
            projects.append(Project(project['team'], project['jql']))
        return projects
    
    def _get_statuses_as_string(self, statuses: list[str]) -> str:
        return f'({",".join(statuses)})'

    def get_resolved_statuses_as_string(self) -> str:
        return self._get_statuses_as_string(self.resolved_statuses)
    
    def get_backlog_statuses_as_string(self) -> str:
        return self._get_statuses_as_string(self.backlog_statuses)
    
    def get_discarded_statuses_as_string(self) -> str:
        return self._get_statuses_as_string(self.discarded_statuses)