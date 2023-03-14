from ..config.config import Config
from ..printer.log import print_header, print_info, print_debug
from ..client.jira_client import JiraClient
    
def show_project_wastages(config: Config, jira_client: JiraClient) -> None:
    print_header(f'Wastage report for the past {config.weeks} weeks')
    print_debug('')
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        print_debug(f'\tJQL: {project.jql}')
        completed = jira_client.get_completed_tickets(config, project.jql)
        wasted = jira_client.get_discarded_tickets(config, project.jql)
        wastage_rate = len(wasted) / (len(completed) + len(wasted)) * 100
        print_info(f'\tWastage rate: {wastage_rate:.2f}%')
        print_debug('')