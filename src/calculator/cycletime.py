import datetime
from ..config.config import Config
from ..printer.log import print_debug, print_header, print_info
from ..client.jira_client import JiraClient


def get_creation_date(ticket) -> datetime:
    if "fields" in ticket and "created" in ticket["fields"] and ticket["fields"]["created"]:
        return datetime.datetime.strptime(ticket["fields"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
    raise ValueError('Ticket has no created date')


def get_resolution_date(resolved_statuses, ticket) -> datetime.datetime:
    if ticket["fields"]["resolutiondate"] and ticket["fields"]["resolutiondate"] != "null" and\
            ticket["fields"]["resolutiondate"] != "None":
        return datetime.datetime.strptime(ticket["fields"]["resolutiondate"], "%Y-%m-%dT%H:%M:%S.%f%z")
    transitions = ticket["changelog"]["histories"]
    for transition in transitions:
        for item in transition["items"]:
            if item["field"] == "status":
                if item["toString"] in resolved_statuses:
                    return datetime.datetime.strptime(transition["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
    raise Warning(f'Ticket {ticket["key"]} has no resolution date')


def get_cycle_time(resolved_statuses, ticket) -> float:
    resolution_date = get_resolution_date(resolved_statuses, ticket)
    creation_date = get_creation_date(ticket)
    if creation_date > resolution_date:
        raise Warning(f'Ticket {ticket["key"]} has a resolution date before the creation date')
    return (resolution_date - creation_date).days


def calculate_average_cycle_time(resolved_statuses, debug_enabled, tickets) -> float:
    if tickets is None or len(tickets) == 0:
        raise Warning('No tickets found')
    total_cycle_time = 0
    for ticket in tickets:
        cycle_time = get_cycle_time(resolved_statuses, ticket)
        total_cycle_time += cycle_time
        if debug_enabled:
            print_debug(f'\t\tTicket {ticket["key"]} took {cycle_time} days to complete')
    return total_cycle_time / len(tickets)


def calculate_percentile_cycle_time(resolved_statuses: list[str], tickets, percentile) -> float:
    cycle_times = []
    for ticket in tickets:
        cycle_time = get_cycle_time(resolved_statuses, ticket)
        cycle_times.append(cycle_time)
    cycle_times.sort()
    index = int(len(cycle_times) * percentile)
    return cycle_times[index]


def show_project_cycletimes(config: Config, jira_client: JiraClient, percentiles: bool = False) -> None:
    print_header(f'Cycletime report for the past {config.weeks} weeks')
    print_debug('')
    for project in config.projects:
        print_info(f'Getting tickets for {project.team}')
        print_debug(f'\tJQL: {project.jql}')
        tickets = jira_client.get_completed_tickets(config, project.jql)
        print_debug(f'\tTickets found: {len(tickets)}')
        print_info(f'\tAverage cycle time: {calculate_average_cycle_time(config.resolved_statuses, config.debug_enabled, tickets):.2f} days')
        if percentiles:
            resolved_statuses = config.resolved_statuses
            print_info(
                f'\t50th percentile cycle time: {calculate_percentile_cycle_time(resolved_statuses, tickets, 0.50):.2f} days')
            print_info(
                f'\t75th percentile cycle time: {calculate_percentile_cycle_time(resolved_statuses, tickets, 0.75):.2f} days')
            print_info(
                f'\t85th percentile cycle time: {calculate_percentile_cycle_time(resolved_statuses, tickets, 0.85):.2f} days')
        print_debug('')
