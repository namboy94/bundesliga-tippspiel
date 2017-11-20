# get_user_bets_for_matchday

Retrieves the existing bets for a user for a given matchday

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
        "data": [Bet]
    }
    
```

## Data:

A Bet consists of the following values:

```json
    {
        "id": INT,
        "home_score": INT,
        "away_score": INT,
        "match": MATCH
    }
```

Refer to [get_matches_for_matchday](get_matches_for_matchday.md) to see what a
match consists of.