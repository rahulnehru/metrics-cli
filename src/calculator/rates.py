import datetime
from ..config.config import Config
from ..printer.log import print_info, print_debug, print_warning, print_header, br
from ..client.jira_client import JiraClient


def get_number_of_working_days_in_past_weeks(config: Config) -> int:
    today = datetime.date.today()
    start_date = today - datetime.timedelta(weeks=config.weeks)
    number_of_working_days = 0
    for day in range((today - start_date).days + 1):
        date = start_date + datetime.timedelta(days=day)
        if date.weekday() < 5:
            number_of_working_days += 1
    return number_of_working_days


def calculate_rate(tickets: int, number_of_working_days: int) -> float:
    if number_of_working_days == 0:
        raise ValueError('No working days found')
    return tickets / number_of_working_days


def show_project_rates(config: Config, jira_client: JiraClient) -> None:
    print_header(f'Entry/departure report for the past {config.weeks} weeks')
    br()
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        if config.debug_enabled:
            print_debug(f'JQL: {project.jql}')
        total_completed = len(jira_client.get_completed_tickets(config, project.jql)) + \
                          len(jira_client.get_discarded_tickets(config, project.jql))
        tickets_raised = len(jira_client.get_raised_tickets(config, project.jql))
        number_of_working_days = get_number_of_working_days_in_past_weeks(config)
        tickets_raised_per_day = calculate_rate(tickets_raised, number_of_working_days)
        tickets_completed_per_day = calculate_rate(total_completed, number_of_working_days)
        if config.debug_enabled:
            print_debug(f'Tickets raised: {tickets_raised}')
            print_debug(f'Tickets completed or closed: {total_completed}')
            print_debug(f'Number of working days: {number_of_working_days}')
        print_info(f'Entry rate: {tickets_raised_per_day:.2f}')
        print_info(f'Exit rate: {tickets_completed_per_day:.2f}')
        if tickets_raised_per_day > tickets_completed_per_day:
            print_warning(f'WIP is increasing')
        br()
    br()

