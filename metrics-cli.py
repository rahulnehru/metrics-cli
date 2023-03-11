from client.jira_client import JiraClient
from config.config import Config
import calculator.cycletime
import calculator.throughput
import calculator.wastage
import calculator.wip
import click
import hvac

client = hvac.Client()

@click.group()
def cli():
    pass

@click.command(help = "Generate cycle time report for projects")
@click.argument("username", required=True, type=str, help="Jira username")
@click.argument("password", required=True, type=str, help="Jira password")
@click.argument("config", required=True, type=str, help="Path to config file")
@click.option("--weeks", default=3, help="Number of weeks to look back")
def cycletime(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    calculator.cycletime.show_project_cycletimes(config, jira_client)

@click.command(help = "Generate throughput report for projects")
@click.argument("username", required=True, type=str, help="Jira username")
@click.argument("password", required=True, type=str, help="Jira password")
@click.argument("config", required=True, type=str, help="Path to config file")
@click.option("--weeks", default=3, help="Number of weeks to look back")
def throughput(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    calculator.throughput.show_project_throughputs(config, jira_client)  

@click.command(help = "Generate work-in-progress report for projects")
@click.argument("username", required=True, type=str, help="Jira username")
@click.argument("password", required=True, type=str, help="Jira password")
@click.argument("config", required=True, type=str, help="Path to config file")
def wip(config, username, password):
    config = Config(config, None)
    jira_client = JiraClient(username, password, config.jira_url)
    calculator.wip.show_project_wips(config, jira_client)    

@click.command(help = "Wastage report for projects")
@click.argument("username", required=True, type=str, help="Jira username")
@click.argument("password", required=True, type=str, help="Jira password")
@click.argument("config", required=True, type=str, help="Path to config file")
@click.option("--weeks", default=3, help="Number of weeks to look back")
def wastage(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    calculator.wastage.show_project_wastages(config, jira_client)

@click.command(help = "Generate all reports for projects")
@click.argument("username", required=True, type=str, help="Jira username")
@click.argument("password", required=True, type=str, help="Jira password")
@click.argument("config", required=True, type=str, help="Path to config file")
@click.option("--weeks", default=3, help="Number of weeks to look back")
def all(config, username, password, weeks):
    config = Config(config, weeks)
    jira_client = JiraClient(username, password, config.jira_url)
    calculator.cycletime.show_project_cycletimes(config, jira_client)
    calculator.throughput.show_project_throughputs(config, jira_client)
    calculator.wastage.show_project_wastages(config, jira_client)
    calculator.wip.show_project_wips(config, jira_client)    

def main():
    cli.add_command(cycletime)
    cli.add_command(throughput)
    cli.add_command(wip)
    cli.add_command(wastage)
    cli.add_command(all)
    cli()

if __name__ == '__main__':
    main()    
    
