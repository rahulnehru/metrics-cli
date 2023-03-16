from ..config.config import Config
from ..printer.log import print_header, print_info, print_debug
from ..client.jira_client import JiraClient


def show_project_throughputs(config: Config, jira_client: JiraClient) -> None:
    print_header(f'Throughput report for the past {config.weeks} weeks')
    print_debug('')
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        print_debug(f'\tJQL: {project.jql}')
        tickets = jira_client.get_completed_tickets(config, project.jql)
        print_info(f'\tTickets found: {len(tickets)}')
        print_debug('')
