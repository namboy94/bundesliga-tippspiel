# get_goal_data_for_match

Retrieves all goals for a match.

## Input:

```json
    {
        "username": "VALUE",
        "api_key": "VALUE",
        "match_id": INT
    }
```  

## Response:

```json
    {
        "status": "success",
        "data": [Goal]
    }
    
```

## Data:

A Goal consists of the following values:

```json
    {
        "id": INT,
        "minute": INT,
        "penalty": BOOLEAN,
        "owngoal": BOOLEAN,
        "home_score": INT,
        "away_score": INT,
        "match": INT,
        "player": INT
    }
```

A player consists of the following values:

```json
    {
        "id": INT,
        "name": STRING,
        "team": INT
    }
```
