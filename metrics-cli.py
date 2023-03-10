import argparse
from client.jira_client import JiraClient
from config.config import Config
import calculator.cycletime
import calculator.throughput
import click
import hvac

client = hvac.Client()

@click.group()
def cli():
    pass

@click.command(help = "Generate cycle time report for projects")
@click.argument("username")
@click.argument("password")
@click.argument("config")
@click.option("--weeks", default=3, help="Number of weeks to look back")
def cycletime(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    calculator.cycletime.show_project_cycletimes(config, jira_client)

@click.command(help = "Generate throughput report for projects")
@click.argument("username")
@click.argument("password")
@click.argument("config")
@click.option("--weeks", default=3, help="Number of weeks to look back")
def throughput(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    calculator.throughput.show_project_throughputs(config, jira_client)  

def main():
    cli.add_command(cycletime)
    cli.add_command(throughput)
    cli()

if __name__ == '__main__':
    main()    
    
