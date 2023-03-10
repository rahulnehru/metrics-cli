import yaml
from config.project import Project

class Config:
    jira_url: str
    resolved_statuses: list[str]
    projects: list[Project]
    weeks: int

    def __init__(self, config_file: str, weeks: int):
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.jira_url = config['jira']['url']
            self.resolved_statuses = config['jira']['resolved_statuses']
            self.projects = self._map_to_projects(config['projects'])
            self.debug_enabled = config['debug_enabled']
            self.weeks = weeks

    def _map_to_projects(self, projects_dict):
        projects = []
        for project in projects_dict:
            projects.append(Project(project['team'], project['jql']))
        return projects

    def get_resolved_statuses_as_string(self):
        return f'({",".join(self.resolved_statuses)})'