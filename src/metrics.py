from .client.jira_client import JiraClient
from .config.config import Config
from .calculator.cycletime import show_project_cycletimes
from .calculator.throughput import show_project_throughputs
from .calculator.wastage import show_project_wastages
from .calculator.rates import show_project_rates
from .calculator.wip import show_project_wips
import click
import hvac

client = hvac.Client()

@click.group()
def cli():
    pass

@click.command(help = "Generate cycle time report for projects")
@click.argument("username", required=True, type=str)
@click.argument("password", required=True, type=str)
@click.argument("config", required=True, type=str)
@click.option("--weeks", default=3, help="Number of weeks to look back")
@click.option("--percentiles", default=False, help="Include percentiles in report")
def cycletime(config, username, password, weeks, percentiles):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    show_project_cycletimes(config, jira_client, percentiles)

@click.command(help = "Generate throughput report for projects")
@click.argument("username", required=True, type=str)
@click.argument("password", required=True, type=str)
@click.argument("config", required=True, type=str)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def throughput(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    show_project_throughputs(config, jira_client)  

@click.command(help = "Generate work-in-progress report for projects")
@click.argument("username", required=True, type=str)
@click.argument("password", required=True, type=str)
@click.argument("config", required=True, type=str)
def wip(config, username, password):
    config = Config(config, None)
    jira_client = JiraClient(username, password, config.jira_url)
    show_project_wips(config, jira_client)    

@click.command(help = "Wastage report for projects")
@click.argument("username", required=True, type=str)
@click.argument("password", required=True, type=str)
@click.argument("config", required=True, type=str)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def wastage(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    show_project_wastages(config, jira_client)

@click.command(help = "Generate entry and departure rate for projects")
@click.argument("username", required=True, type=str)
@click.argument("password", required=True, type=str)
@click.argument("config", required=True, type=str)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def rates(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    rates.show_project_rates(config, jira_client)    

@click.command(help = "Generate all reports for projects")
@click.argument("username", required=True, type=str)
@click.argument("password", required=True, type=str)
@click.argument("config", required=True, type=str)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def all(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    show_project_cycletimes(config, jira_client)
    show_project_throughputs(config, jira_client)
    show_project_wastages(config, jira_client)
    show_project_wips(config, jira_client)       
    rates.show_project_rates(config, jira_client) 

def main():
    cli.add_command(cycletime)
    cli.add_command(throughput)
    cli.add_command(wip)
    cli.add_command(wastage)
    cli.add_command(rates)
    cli.add_command(all)
    cli()

if __name__ == '__main__':
    main()    
    
