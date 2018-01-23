# get_bets_for_match

Retrieves all bets for a match. If the match hasn't started yet, 
Only the authenticated user's bet will be sent.

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
        "match": INT,
        "points": INT
    }
```
