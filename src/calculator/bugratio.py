from ..config.config import Config
from ..printer.log import print_header, print_info, print_debug, br
from ..client.jira_client import JiraClient


def calculate_wastage(completed_tickets: list[dict], discarded_tickets: list[dict]) -> float:
    if len(completed_tickets) == 0 and len(discarded_tickets) == 0:
        raise ValueError('No tickets found')
    return len(discarded_tickets) / (len(completed_tickets) + len(discarded_tickets)) * 100


def show_project_bug_ratio(config: Config, jira_client: JiraClient) -> None:
    print_header(f'Bug ratio report for the past {config.weeks} weeks')
    br()
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        if config.debug_enabled:
            print_debug(f'JQL: {project.jql}')
        raised = jira_client.get_raised_tickets(config, project.jql)

        bug_types = config.bug_types
        bug_tickets = len([ticket for ticket in raised if ticket['fields']['issuetype']['name'] in bug_types])
        total_tickets = len(raised)

        print_info(f'Bug ratio: {(bug_tickets / total_tickets * 100):.2f}%')
        br()
    br()
