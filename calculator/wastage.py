from config.config import Config
import printer.log as log
from client.jira_client import JiraClient
    
def show_project_wastages(config: Config, jira_client: JiraClient):
    log.print_header(f'Wastage report for the past {config.weeks} weeks')
    print('')
    for project in config.projects:
        log.print_info(f'Getting tickets for {project.team}')
        log.print_debug(f'\tJQL: {project.jql}')
        completed = jira_client.get_completed_tickets(config, project.jql)
        wasted = jira_client.get_discarded_tickets(config, project.jql)
        wastage_rate = len(wasted) / (len(completed) + len(wasted)) * 100
        log.print_info(f'\tWastage rate: {wastage_rate:.2f}%')
        print('')