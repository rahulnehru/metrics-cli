import requests
from requests.auth import HTTPBasicAuth
from ..config.config import Config
from ..printer.log import print_error
import multiprocessing

class JiraClient:
    username: str
    password: str
    base_url: str
    session: requests.Session

    def __init__(self, username: str, password: str, base_url: str) -> None:
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = requests.Session()

    def _run_jira_query(self, jql: str, startAt: int) -> list[dict]:
        jira_data = {
            "jql": jql,
            "startAt": startAt,
            "maxResults": 50,
            "expand": "changelog"
        }
        response = requests.get(self.base_url, auth=HTTPBasicAuth(self.username, self.password), params=jira_data, stream=True)
        if response.status_code != 200:
            print_error(f'Error: {response.status_code}')
            print_error(response.text)
            exit(-1)
        return response.json()    
    
    def _get_tickets(self, jql: str) -> list[dict]:
        tickets = []
        page = 0
        total_matches = self._run_jira_query(jql, page)['total']
        pages = total_matches // 50
        with multiprocessing.Pool(pages + 1) as pool:
            tickets = pool.starmap(self._run_jira_query, [(jql, page * 50) for page in range(0, pages + 1)])
        tickets = [ticket for page in tickets for ticket in page['issues']]
        pool.close()
        return tickets
    

    def get_completed_tickets(self, config: Config, jql: str) -> list[dict]:
        completed_ticket_jql = f'{jql} AND status changed to {config.get_resolved_statuses_as_string()} AFTER -{config.weeks}w'
        return self._get_tickets(completed_ticket_jql)
    
    def get_inflight_tickets(self, config: Config, jql: str) -> list[dict]:
        inflight_ticket_jql = f'{jql} AND status not in {config.get_resolved_statuses_as_string()} and status not in {config.get_backlog_statuses_as_string()} and status not in {config.get_discarded_statuses_as_string()}'
        return self._get_tickets(inflight_ticket_jql)
    
    def get_discarded_tickets(self, config: Config, jql: str) -> list[dict]:
        discarded_ticket_jql = f'{jql} AND status changed to {config.get_discarded_statuses_as_string()} AFTER -{config.weeks}w'
        return self._get_tickets(discarded_ticket_jql)
    
    def get_raised_tickets(self, config: Config, jql: str) -> list[dict]:
        raised_ticket_jql = f'{jql} AND status changed from {config.get_backlog_statuses_as_string()} AFTER -{config.weeks}w'
        return self._get_tickets(raised_ticket_jql)