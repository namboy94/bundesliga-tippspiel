# place_bets

Allows you to place one or more bets. Invalid bets are automatically rejected,
so make sure that all of the following is true for the input:

* The "home_score" value is set and an integer between 0 and 99
* The "away_score" value is set and an integer between 0 and 99
* The "match_id" value is set and an integer that maps to a valid match

Bets for matches that have already started are automatically ignored.

```json
    {
        "username": "VALUE",
        "api_key": "VALUE",
        "bets": [
            {
                "home_score": INT,
                "away_score": INT,
                "match_id": INT
            }
            ...
        ]
    }
```
    
## Response:

All bets OK:

```json
    {
        "status": "success"
    }
```

Bets for matches that have started:

```json
    {
        "status": "success_with_errors"
    }
```

For invalid bet:

```json
    {
        "status": "error",
        "cause": "invalid_bet"
    }
```