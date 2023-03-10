import yaml
from config.project import Project

class Config:
    jira_url: str
    resolved_statuses: list[str]
    projects: list[Project]

    def __init__(self, config_file):
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.jira_url = config['jira']['url']
            self.resolved_statuses = config['jira']['resolved_statuses']
            self.projects = config['projects']
            self.debug_enabled = config['debug_enabled']

    def get_resolved_statuses_as_string(self):
        return f'({",".join(self.resolved_statuses)})'