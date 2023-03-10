from config.config import Config
import printer.log as log
from client.jira_client import JiraClient


def show_project_throughputs(config: Config, jira_client: JiraClient):
    log.print_header(f'Throughput report for the past {config.weeks} weeks')
    print('')
    for project in config.projects:
        log.print_info(f'Getting tickets for {project.team}')
        log.print_debug(f'\tJQL: {project.jql}')
        tickets = jira_client.get_tickets(config, project.jql)
        log.print_info(f'\tTickets found: {len(tickets)}')
        print('')