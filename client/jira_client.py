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
        jira_data = {
            "jql": jql,
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
    
    def _get_tickets(self, config: Config, jql: str) -> list[dict]:
        tickets = []
        page = 0
        while True:
            results = self._run_jira_query(config, jql, page)
            if len(results) == 0:
                break
            page += 50
            tickets.extend(results)
        return tickets
    

    def get_completed_tickets(self, config: Config, jql: str) -> list[dict]:
        completed_ticket_jql = f'{jql} AND status changed to {config.get_resolved_statuses_as_string()} AFTER -{config.weeks}w'
        return self._get_tickets(config, completed_ticket_jql)
    
    def get_inflight_tickets(self, config: Config, jql: str) -> list[dict]:
        inflight_ticket_jql = f'{jql} AND status not in {config.get_resolved_statuses_as_string()} and status not in {config.get_backlog_statuses_as_string()} and status not in {config.get_discarded_statuses_as_string()}'
        return self._get_tickets(config, inflight_ticket_jql)
    
    def get_discarded_tickets(self, config: Config, jql: str) -> list[dict]:
        discarded_ticket_jql = f'{jql} AND status changed to {config.get_discarded_statuses_as_string()} AFTER -{config.weeks}w'
        return self._get_tickets(config, discarded_ticket_jql)
    
    def get_raised_tickets(self, config: Config, jql: str) -> list[dict]:
        raised_ticket_jql = f'{jql} AND status changed from {config.get_backlog_statuses_as_string()} AFTER -{config.weeks}w'
        return self._get_tickets(config, raised_ticket_jql)