class Project:
    team: str
    jql: str

    def __init__(self, team, jql) -> None:
        self.team = team
        self.jql = jql

    def __str__(self) -> str:
        return f'{self.team}: {self.jql}'
