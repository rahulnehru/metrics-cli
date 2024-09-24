from ..config.config import Config
from ..printer.log import print_header, print_info, print_debug, br
from ..client.jira_client import JiraClient


def show_project_throughputs(config: Config, jira_client: JiraClient) -> None:
    print_header(f'Throughput report for the past {config.weeks} weeks')
    br()
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        if config.debug_enabled:
            print_debug(f'JQL: {project.jql}')
        tickets = jira_client.get_completed_tickets(config, project.jql)
        print_info(f'Tickets completed in {config.weeks} weeks: {len(tickets)}')
        br()
    br()
