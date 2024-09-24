import requests
from requests import Response
from requests.auth import HTTPBasicAuth
from ..config.config import Config
from ..printer.log import print_error, print_warning
import multiprocessing
import resource


def wrap_connection_exception(f, host):
    try:
        return f()
    except requests.exceptions.ConnectionError:
        print_error(f"Could not connect to host {host}")
        exit(-1)


def handle_error(response: Response):
    if response.status_code > 299:
        print_error(f"Could not execute request: {response.status_code}")
        print_error(response.text)
        exit(-1)


class JiraClient:
    auth_token: str
    base_url: str
    session: requests.Session
    page_size: int

    def __init__(self, auth_token: str, base_url: str) -> None:
        self.auth_token = auth_token
        self.base_url = base_url
        self.session = requests.Session()
        self.page_size = 1

    def __configure_page_size(self, number_of_tickets: int) -> None:
        files_available = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
        min_page_size = number_of_tickets // files_available
        if min_page_size > self.page_size:
            new_page_size = int(number_of_tickets / files_available) + 1
            print_warning(f"Will need to optimise number of tickets in a page for performance reasons from {self.page_size} to {new_page_size}")
            self.page_size = new_page_size

    @staticmethod
    def auth(base_url, username, password) -> dict:
        content_type_header = {'Content-Type': 'application/json'}
        response = wrap_connection_exception(lambda: requests.post(f'{base_url}/rest/pat/latest/tokens',
                                                                   headers=content_type_header,
                                                                   data='{"name": "metrics", "expirationDuration": 90}',
                                                                   auth=HTTPBasicAuth(username, password)), base_url)
        handle_error(response)
        return response.json()

    def _run_jira_query(self, jql: str, start_at: int) -> dict:
        jira_data = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": self.page_size,
            "expand": "changelog"
        }
        header = {'Authorization': f'Bearer {self.auth_token}'}
        response = wrap_connection_exception(lambda: self.session.get(f'{self.base_url}/rest/api/2/search',
                                                                      headers=header, params=jira_data,
                                                                      stream=True), self.base_url)
        handle_error(response)
        return response.json()

    def _get_tickets(self, jql: str) -> list[dict]:
        page = 0
        total_matches = self._run_jira_query(jql, page)['total']
        self.__configure_page_size(total_matches)
        pages = total_matches // self.page_size
        with multiprocessing.Pool(pages + 1) as pool:
            tickets = pool.starmap(self._run_jira_query, [(jql, page * self.page_size) for page in range(0, pages + 1)])
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
