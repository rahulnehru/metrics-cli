from ..config.config import Config
from ..printer.log import print_header, print_info, print_debug, br
from ..client.jira_client import JiraClient

k_status = 'status'
k_fields = 'fields'
k_name = 'name'


def group_tickets_by_status(tickets: list[dict]) -> dict[str, int]:
    grouped_tickets = {}
    for ticket in tickets:
        status = ticket[k_fields][k_status][k_name]
        if status not in grouped_tickets:
            grouped_tickets[status] = 0
        grouped_tickets[status] += 1
    return grouped_tickets


def show_project_wip(config: Config, jira_client: JiraClient) -> None:
    print_header('Work in Progress report')
    br()
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        if config.debug_enabled:
            print_debug(f'JQL: {project.jql}')
        tickets = jira_client.get_inflight_tickets(config, project.jql)
        grouped_tickets = group_tickets_by_status(tickets)
        for status in grouped_tickets:
            if config.debug_enabled:
                print_debug(f'{status}: {grouped_tickets[status]}')
        print_info(f'Tickets found: {len(tickets)}')
        br()
    br()