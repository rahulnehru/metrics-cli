# Metrics CLI 

This tool can be used to get Agile metrics for a limited period of time for your teams from Jira. This currently only supports the v2 Jira REST API. 

## Running locally
This tool can be run natively by using the install script, or using Docker.
### Running using Docker

### Running locally

## Configuration
You must specify a YAML configuration file which contains the details of your Jira instance and the projects you are interested in:

```yaml
jira:
  url: "https://jira.atlassian.com/rest/api/2/search"
  statuses:
    resolved:
      - Live
      - Done
      - Resolved
    backlog:
      - Backlog
      - New
    discarded:
      - Withdrawn
      - Closed  

debug_enabled: false

projects:
  - team: "Project Team 1 Stories"
    jql: 'project = "APP" AND "Assigned Team" = "PT1" and issueType = Story'
  - team: "Project Team 2"
    jql: 'project = "APP" AND "Assigned Team" = "PT3"'
  - team: "Project Team 3"
    jql: 'project = "APP" AND "Assigned Team" = "PT3"'
  
```

## Metrics supported 

### Cycletime
Cycletime is the length of time taken to complete work items. This tool calculates the cycletime from the point that an issue was created in Jira, to the point it's status was changed to one of the resolved statuses defined in your YAML configuration file.

The output includes an average cycletime, as well as a 50th, 75th and 85th percentile.

The way to read these metrics is:
* "On average, a ticket is completed in X days" (where X is the average)
* "85% of the time, Team 1 completed their tickets in Y days or less" (where Y is the 85th percentile)

### Throughput
Throughput is a measure of the number of items completed in a given time period. 

### Work In Progress
Work in progress is the amount of items which are currently in-flight. This tool calculates WIP as the number of items which are not in a backlog state, or resolved and discarded status (as defined in your config file).

The generated report will also list out the number of items in each workflow stage. 

### Entry / Departure Rates
The entry rate is defined as the number of items entering the workflow (not the backlog state) per working day.

The exit/departure rate is defined as the number of items being completed by the workflow.

The generated report analyses the entry and exit rates over the specified time period. This metric is useful to understand whether the Work in Progress has grown over the specified time period (i.e. the team is doing more work in parallel than at the start of the period).

### Wastage
The wastage report is used to analyse the ratio of how many tickets are being completed rather than rejected or discareded during the specified period. 
