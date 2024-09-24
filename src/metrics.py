from pathlib import Path
from .client.jira_client import JiraClient
from .config.config import Config
from .calculator.cycletime import show_project_cycletimes
from .calculator.throughput import show_project_throughputs
from .calculator.wastage import show_project_wastages
from .calculator.rates import show_project_rates
from .calculator.wip import show_project_wip
from .calculator.bugratio import show_project_bug_ratio
from .auth.auth_config import append_token_to_auth_server_file, read_token_from_yaml_file, AuthServer
from .printer.log import print_error, print_info
import click
import hvac
import os
import yaml

client = hvac.Client()


@click.group()
def cli() -> None:
    pass


_default_directory = os.path.join(os.path.expanduser("~"), ".jira_metrics")
_auth_filename = os.path.join(_default_directory, "servers.yaml")
_config_filename = os.path.join(_default_directory, "config.yaml")


def read_default_config_file() -> Config:
    return Config(_config_filename, 3)


def create_config_folder() -> None:
    if not os.path.exists(_default_directory):
        print_error(f"No configuration folder found. Creating one in... {_default_directory}")
        Path(_default_directory).mkdir(parents=True, exist_ok=True)


def create_default_files() -> None:
    if not os.path.exists(_auth_filename):
        print_error(f"No authentication file found. Creating one in... {_auth_filename}")
        Path(_auth_filename).touch()
        with open(_auth_filename, 'w') as f:
            yaml.dump(AuthServer.get_yaml_template(), f)
    if not os.path.exists(_config_filename):
        Path(_config_filename).touch()
        print_error(f"No configuration file found. Creating one in... {_config_filename}")
        with open(_config_filename, 'w') as f:
            yaml.dump(Config.get_yaml_template(), f)


def read_authentication_token(jira_url) -> str:
    auth_token = read_token_from_yaml_file(jira_url, _auth_filename)
    if auth_token is None:
        print_error(f"No authentication token found for {jira_url}. Run 'metrics auth' to authenticate.")
        exit(-1)
    return auth_token


@click.command(help="Authenticate with Jira")
@click.option("--username", prompt=True, required=True, type=str)
@click.option("--password", prompt=True, required=True, type=str, hide_input=True)
@click.argument("jira-url", required=True, type=str, default=lambda: read_default_config_file().jira_url)
def auth(username, password, jira_url) -> None:
    print_info(f"Authenticating with {jira_url}")
    token = JiraClient.auth(jira_url, username, password)['rawToken']
    append_token_to_auth_server_file(f'{_default_directory}/servers.yaml', jira_url, token)
    print_info('Authentication successful!')


@click.command(help="Generate cycle time report for projects")
@click.argument("config", required=True, type=str, default=_config_filename)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def cycletime(config, weeks) -> None:
    config = Config(config, weeks)
    auth_token = read_authentication_token(config.jira_url)
    jira_client = JiraClient(auth_token, config.jira_url)
    show_project_cycletimes(config, jira_client)


@click.command(help="Generate throughput report for projects")
@click.argument("config", required=True, type=str, default=_config_filename)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def throughput(config, weeks) -> None:
    config = Config(config, weeks)
    auth_token = read_authentication_token(config.jira_url)
    jira_client = JiraClient(auth_token, config.jira_url)
    show_project_throughputs(config, jira_client)


@click.command(help="Generate work-in-progress report for projects")
@click.argument("config", required=True, type=str, default=_config_filename)
def wip(config) -> None:
    config = Config(config, None)
    auth_token = read_authentication_token(config.jira_url)
    jira_client = JiraClient(auth_token, config.jira_url)
    show_project_wip(config, jira_client)


@click.command(help="Wastage report for projects")
@click.argument("config", required=True, type=str, default=_config_filename)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def wastage(config, weeks) -> None:
    config = Config(config, weeks)
    auth_token = read_authentication_token(config.jira_url)
    jira_client = JiraClient(auth_token, config.jira_url)
    show_project_wastages(config, jira_client)


@click.command(help="Generate entry and departure rate for projects")
@click.argument("config", required=True, type=str, default=_config_filename)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def rates(config, weeks) -> None:
    config = Config(config, weeks)
    auth_token = read_authentication_token(config.jira_url)
    jira_client = JiraClient(auth_token, config.jira_url)
    show_project_rates(config, jira_client)


@click.command(help="Generate bug ratio for projects")
@click.argument("config", required=True, type=str, default=_config_filename)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def bugratio(config, weeks) -> None:
    config = Config(config, weeks)
    auth_token = read_authentication_token(config.jira_url)
    jira_client = JiraClient(auth_token, config.jira_url)
    show_project_bug_ratio(config, jira_client)


@click.command(help="Generate all reports for projects")
@click.argument("config", required=True, type=str, default=_config_filename)
@click.option("--weeks", default=3, help="Number of weeks to look back")
def all(config, weeks) -> None:
    config = Config(config, weeks)
    auth_token = read_authentication_token(config.jira_url)
    jira_client = JiraClient(auth_token, config.jira_url)
    show_project_cycletimes(config, jira_client)
    show_project_throughputs(config, jira_client)
    show_project_wastages(config, jira_client)
    show_project_wip(config, jira_client)
    show_project_rates(config, jira_client)


def main() -> None:
    create_config_folder()
    create_default_files()
    cli.add_command(auth)
    cli.add_command(cycletime)
    cli.add_command(throughput)
    cli.add_command(wip)
    cli.add_command(wastage)
    cli.add_command(rates)
    cli.add_command(all)
    cli.add_command(bugratio)
    cli()


if __name__ == '__main__':
    main()
