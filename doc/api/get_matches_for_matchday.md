# authorize

Retrieves match information for all matches on a particular matchday.

## Input:

```json
    {
        "username": "VALUE",
        "api_key": "VALUE",
        "matchday": INT
    }
```

or for current matchday:

```json
    {
        "username": "VALUE",
        "api_key": "VALUE"
    }
```
    
## Response:

```json
    {
        "status": "success",
        "data": [Match]
    }
```

# Data

List of matches. A single match contains the following values:


```json
    {
    "id": INT,
    "home_team": TEAM,
    "away_team": TEAM,
    "home_ht_score": INT,
    "away_ht_score": INT,
    "home_ft_score": INT,
    "away_ft_score": INT,
    "matchday": INT,
    "kickoff": "YYYY-MM-DDThh:mm:ssZ",
    "finished": BOOL,
    "started": BOOL
    }
```

A Team consists of the following values:

```json
    {
    "id": INT,
    "name": "VALUE",
    "shortname": "VALUE",
    "abbreviation": "VALUE",
    "icon": "VALUE"
    }
```