import os
import yaml


def read_token_from_yaml_file(jira_url: str, file_path: str) -> str | None:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            return next((server['token'] for server in data if server['jira_url'] == jira_url), None)
    raise Warning("No token found for this Jira instance")


def append_token_to_auth_server_file(file_path: str, jira_url: str, token: str) -> None:
    with open(file_path, "w+") as f:
        auth_servers = yaml.safe_load(f)
        if auth_servers is None:
            auth_servers = []
        if len(auth_servers) > 0:
            for server in auth_servers:
                if server['jira_url'] == jira_url:
                    server['token'] = token
                    break
        else:
            auth_servers.append({'jira_url': jira_url, 'token': token})
        f.truncate()
        yaml.dump(auth_servers, f)


class AuthServer:
    jira_url: str
    token: str

    def __init__(self, jira_url: str, token: str) -> None:
        self.jira_url = jira_url
        self.token = token

