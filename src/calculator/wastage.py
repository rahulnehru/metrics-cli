from ..config.config import Config
from ..printer.log import print_header, print_info, print_debug, br
from ..client.jira_client import JiraClient


def calculate_wastage(completed_tickets: list[dict], discarded_tickets: list[dict]) -> float:
    if len(completed_tickets) == 0 and len(discarded_tickets) == 0:
        raise ValueError('No tickets found')
    return len(discarded_tickets) / (len(completed_tickets) + len(discarded_tickets)) * 100


def show_project_wastages(config: Config, jira_client: JiraClient) -> None:
    print_header(f'Wastage report for the past {config.weeks} weeks')
    br()
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        if config.debug_enabled:
            print_debug(f'\tJQL: {project.jql}')
        completed = jira_client.get_completed_tickets(config, project.jql)
        wasted = jira_client.get_discarded_tickets(config, project.jql)
        wastage_rate = calculate_wastage(completed, wasted)
        print_info(f'\tWastage rate: {wastage_rate:.2f}%')
        br()
