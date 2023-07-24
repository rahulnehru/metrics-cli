import datetime
from ..config.config import Config
from ..printer.log import print_debug, print_header, print_info, br
from ..client.jira_client import JiraClient

k_field = "field"
k_fields = "fields"
k_created = "created"
k_resolution_date = "resolutiondate"
k_changelog = "changelog"
k_key = "key"
k_histories = "histories"
k_items = "items"
k_to_string = "toString"
timestamp_fmt = "%Y-%m-%dT%H:%M:%S.%f%z"


def get_creation_date(ticket) -> datetime:
    if k_fields in ticket and k_created in ticket[k_fields] and ticket[k_fields][k_created]:
        return datetime.datetime.strptime(ticket[k_fields][k_created], timestamp_fmt)
    raise ValueError('Ticket has no created date')


def get_resolution_date(resolved_statuses, ticket) -> datetime.datetime:
    if ticket[k_fields][k_resolution_date] and ticket[k_fields][k_resolution_date] != "null" and \
            ticket[k_fields][k_resolution_date] != "None":
        return datetime.datetime.strptime(ticket[k_fields][k_resolution_date], timestamp_fmt)
    transitions = ticket[k_changelog][k_histories]
    for transition in transitions:
        for item in transition[k_items]:
            if item[k_field] == "status":
                if item[k_to_string] in resolved_statuses:
                    return datetime.datetime.strptime(transition[k_created], timestamp_fmt)
    raise Warning(f'Ticket {ticket[k_key]} has no resolution date')


def get_cycle_time(resolved_statuses, ticket) -> float:
    resolution_date = get_resolution_date(resolved_statuses, ticket)
    creation_date = get_creation_date(ticket)
    if creation_date > resolution_date:
        raise Warning(f'Ticket {ticket[k_key]} has a resolution date before the creation date')
    return (resolution_date - creation_date).days


def calculate_ave_cycletime(config, tickets) -> float:
    if tickets is None or len(tickets) == 0:
        raise Warning('No tickets found')
    total_cycle_time = 0
    for ticket in tickets:
        cycle_time = get_cycle_time(config.resolved_statuses, ticket)
        total_cycle_time += cycle_time
        if config.debug_enabled:
            print_debug(f'Ticket {ticket[k_key]} took {cycle_time} days to complete')
    return total_cycle_time / len(tickets)


def calculate_percentile_cycle_time(resolved_statuses: list[str], tickets, percentile) -> float:
    cycle_times = []
    for ticket in tickets:
        cycle_time = get_cycle_time(resolved_statuses, ticket)
        cycle_times.append(cycle_time)
    cycle_times.sort()
    index = int(len(cycle_times) * percentile)
    return cycle_times[index]


def show_project_cycletimes(config: Config, jira_client: JiraClient) -> None:
    print_header(f'Cycletime report for the past {config.weeks} weeks')
    br()
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        if config.debug_enabled:
            print_debug(f'\tJQL: {project.jql}')
        tickets = jira_client.get_completed_tickets(config, project.jql)
        if config.debug_enabled:
            print_debug(f'\tTickets found: {len(tickets)}')
        print_info(f'\tAve cycletime: {calculate_ave_cycletime(config, tickets):.2f} days')
        resolved_statuses = config.resolved_statuses
        for percentile in config.cycletime_percentiles:
            print_info(f'\t{percentile} percentile: '
                        f'{calculate_percentile_cycle_time(resolved_statuses, tickets, percentile):.2f} days')
        br()
    br()


