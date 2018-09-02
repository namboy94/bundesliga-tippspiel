# /bet (PUT)

This API endpoint allows placing bets.
For information on how to get bet data, consult the
[bet (GET))](bet-get.md) document.

##### Methods

* PUT

##### Authorization

Required

##### Parameters

* **bets:dict**: A dictionary containing bet entries

The dictionary entries take on the following form:

    "{match_id}-(home|away)": int
    
For a bet to be valid, both ```{match_id}-home``` and ```{match_id}-away```
must be provided.

The following restrictions apply to the score values:

* Valid Integer
* 0 <= score_value < 100

Bets can't be placed once a match has started.

Existing Bets will be updated using the new values

**Examples**:

This will place the bet '2:1' on the match '123'
and the bet '3:0' on the match '100'.


    {
        "123-home": 1,
        "123-away": 2,
        "100-home": 3,
        "100;away": 0
    }

##### Response

* **new**: The amount of newly created bets
* **updated**: The amount of updated bets
* **invalid**: The amount of invalid bets


    {
        "status": "ok",
        "data": {
            "new": int,
            "updated": int,
            "invalid": int
        }
    }

##### Notes

Invalid bets are only skipped and won't throw an error.
