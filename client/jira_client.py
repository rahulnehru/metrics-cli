import requests
from requests.auth import HTTPBasicAuth
from config.config import Config
import printer.log as log

class JiraClient:
    username: str
    password: str
    base_url: str

    def __init__(self, username: str, password: str, base_url: str):
        self.username = username
        self.password = password
        self.base_url = base_url

    def _run_jira_query(self, config: Config, jql: str, page: int) -> list[dict]:
        full_jql = f'{jql} AND status changed to {config.get_resolved_statuses_as_string()} AFTER -{config.weeks}w'
        jira_data = {
            "jql": full_jql,
            "startAt": page,
            "maxResults": 50,
            "expand": "changelog"
        }
        response = requests.get(self.base_url, auth=HTTPBasicAuth(self.username, self.password), params=jira_data)
        if response.status_code != 200:
            log.print_error(f'Error: {response.status_code}')
            log.print_error(response.text)
            exit(-1)
        return response.json()['issues']    
    

    def get_tickets(self, config: Config, jql: str) -> list[dict]:
        tickets = []
        page = 0
        while True:
            results = self._run_jira_query(config, jql, page)
            if len(results) == 0:
                break
            page += 50
            tickets.extend(results)
        return tickets