import datetime
from config.config import Config
from config.project import Project
import printer.log as log
from client.jira_client import JiraClient

def _get_creation_date(ticket):
    return datetime.datetime.strptime(ticket["fields"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")

def _get_resolution_date(resolved_statuses, ticket):
    if ticket["fields"]["resolutiondate"] and ticket["fields"]["resolutiondate"] != "null" and ticket["fields"]["resolutiondate"] != "None":
        return datetime.datetime.strptime(ticket["fields"]["resolutiondate"], "%Y-%m-%dT%H:%M:%S.%f%z")
    transitions = ticket["changelog"]["histories"]
    for transition in transitions:
        for item in transition["items"]:
            if item["field"] == "status":
                if item["toString"] in resolved_statuses:
                    return datetime.datetime.strptime(transition["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
    

def _get_cycle_time(resolved_statuses, ticket):
    return (_get_resolution_date(resolved_statuses, ticket) - _get_creation_date(ticket)).days

def _calculate_average_cycle_time(config, tickets):
    total_cycle_time = 0
    for ticket in tickets:
        cycle_time = _get_cycle_time(config.resolved_statuses, ticket)
        total_cycle_time += cycle_time
        if config.debug_enabled:
            log.print_debug(f'\t\tTicket {ticket["key"]} took {cycle_time} days to complete')
    return total_cycle_time / len(tickets)

def show_project_cycletimes(config: Config, jira_client: JiraClient):
    log.print_header(f'Cycletime report for the past {config.weeks} weeks')
    print('')
    for project in config.projects:
        log.print_info(f'Getting tickets for {project.team}')
        log.print_debug(f'\tJQL: {project.jql}')
        tickets = jira_client.get_tickets(config, project.jql)
        log.print_debug(f'\tTickets found: {len(tickets)}')
        log.print_info(f'\tAverage cycle time: {_calculate_average_cycle_time(config, tickets):.2f} days')
        print('')