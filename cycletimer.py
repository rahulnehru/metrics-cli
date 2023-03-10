import requests
import json
import datetime
from requests.auth import HTTPBasicAuth
import argparse
from config.config import Config


def run_jira_query(config, jql, weeks, username, password, page):
    full_jql = f'{jql} AND status changed to {config.get_resolved_statuses_as_string()} AFTER -{weeks}w'
    jira_data = {
        "jql": full_jql,
        "startAt": page,
        "maxResults": 50,
        "expand": "changelog"
    }
    response = requests.get(config.jira_url, auth=HTTPBasicAuth(username, password), params=jira_data)
    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        print(response.text)
        exit(-1)
    return response.json()['issues']

def get_tickets(config, jql, weeks, username, password) -> list[dict]:
    tickets = []
    page = 0
    while True:
        results = run_jira_query(config, jql, weeks, username, password, page)
        if len(results) == 0:
            break
        page += 50
        tickets.extend(results)
    return tickets
        

def get_creation_date(ticket):
    return datetime.datetime.strptime(ticket["fields"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z")

def get_resolution_date(resolved_statuses, ticket):
    if ticket["fields"]["resolutiondate"] and ticket["fields"]["resolutiondate"] != "null" and ticket["fields"]["resolutiondate"] != "None":
        return datetime.datetime.strptime(ticket["fields"]["resolutiondate"], "%Y-%m-%dT%H:%M:%S.%f%z")
    transitions = ticket["changelog"]["histories"]
    for transition in transitions:
        for item in transition["items"]:
            if item["field"] == "status":
                if item["toString"] in resolved_statuses:
                    return datetime.datetime.strptime(transition["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
    

def get_cycle_time(resolved_statuses, ticket):
    return get_resolution_date(resolved_statuses, ticket) - get_creation_date(ticket)

def calculate_average_cycle_time(config, tickets):
    total_cycle_time = 0
    for ticket in tickets:
        if config.debug_enabled:
            print(f'\t\tTicket {ticket["key"]} took {get_cycle_time(config.resolved_statuses, ticket).days} days to complete')
        total_cycle_time += get_cycle_time(config.resolved_statuses, ticket).days
    return total_cycle_time / len(tickets)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="Username for Jira")
    parser.add_argument("-p", "--password", help="Password for Jira")
    parser.add_argument("-c", "--config", help="Config file")
    parser.add_argument("-w", "--weeks", help="Number of weeks to look back", default=3)
    args = parser.parse_args()
    
    config = Config(args.config)
    
        
    print(f'Cycletime report for the past {args.weeks} weeks')
    print('')
    projects = config.projects
    for project in projects:
        jql = project['jql']
        print(f'Getting tickets for {project["team"]}')
        print(f'\tJQL: {jql}')
        tickets = get_tickets(config, jql, args.weeks, args.username, args.password)
        print(f'\tTickets found: {len(tickets)}')
        print(f'\tAverage cycle time: {calculate_average_cycle_time(config, tickets):.2f} days')

if __name__ == '__main__':
    main()    
    
