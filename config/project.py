class Project:
    
    team: str
    jql: str

    def __init__(self, team, jql):
        self.team = team
        self.jql = jql

    def __str__(self):
        return f'{self.team}: {self.jql}'