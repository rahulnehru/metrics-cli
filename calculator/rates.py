import datetime
from config.config import Config
from config.project import Project
import printer.log as log
from client.jira_client import JiraClient

def _get_number_of_working_days_in_past_weeks(config: Config) -> int:
    today = datetime.date.today()
    start_date = today - datetime.timedelta(weeks=config.weeks)
    number_of_working_days = 0
    for day in range((today - start_date).days + 1):
        date = start_date + datetime.timedelta(days=day)
        if date.weekday() < 5:
            number_of_working_days += 1
    return number_of_working_days

def show_project_rates(config: Config, jira_client: JiraClient):
    log.print_header(f'Entry/departure report for the past {config.weeks} weeks')
    print('')
    for project in config.projects:
        log.print_info(f'Getting tickets for {project.team}')
        log.print_debug(f'\tJQL: {project.jql}')
        tickets_raised = len(jira_client.get_raised_tickets(config, project.jql))
        tickets_completed = len(jira_client.get_completed_tickets(config, project.jql))
        tickets_discarded = len(jira_client.get_discarded_tickets(config, project.jql))
        total_completed = tickets_completed + tickets_discarded
        number_of_working_days = _get_number_of_working_days_in_past_weeks(config)
        tickets_raised_per_day = tickets_raised / number_of_working_days
        tickets_completed_per_day = total_completed / number_of_working_days
        if config.debug_enabled:
            log.print_debug(f'\tTickets raised: {tickets_raised}')
            log.print_debug(f'\tTickets completed or closed: {total_completed}')
            log.print_debug(f'\tNumber of working days: {number_of_working_days}')
        log.print_info(f'\tEntry rate: {tickets_raised_per_day:.2f}')
        log.print_info(f'\tExit rate: {tickets_completed_per_day:.2f}')
        if tickets_raised_per_day > tickets_completed_per_day:
            log.print_warning(f'\t\tWIP is increasing')
        print('')