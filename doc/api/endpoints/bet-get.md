# /bet (GET)

This API endpoint allows fetching bet data.
For information on how to place bets, consult the
[bet (PUT))](bet-put.md) document.

##### Methods

* GET

##### Authorization

Required

##### Parameters

The parameters are all optional and act as filters.

* **user_id:int**: Only returns bets from the specified user
* **match_id:int**: Only returns bets for the specified match
* **matchday:int**: Only returns bets from the specified matchday


To retrieve an element with a specific ID, append /<ID> to the URL.

Examples:

    GET /api/v2/bet                        # All bets
    GET /api/v2/bet/1                      # Bet with ID 1
    GET /api/v2/bet?user_id=3&matchday=17  # Bets for player 3 on matchday 17

##### Response

* **bets:list**: A list of bets
  * **id:int**: The ID of the bet
  * **user_id:int**: The ID of the user that placed this bet
  * **user:<User>**: The user that placed this bet
  * **match_id:int**: The ID of the match that this bet was placed for
  * **match:<Match>**: The match that this bet was placed for
  * **home_score:int**: The score bet on the home team
  * **away_score:int**: The score bet on the away team
* **bet:<Bet>**: A single bet, only available when specific ID was provided


    {
        "status": "ok",
        "data": {
            "bets": [
                {
                    "id": int,
                    "user_id": int,
                    "user": <User>
                    "match_id": int,
                    "match": <Match>,
                    "home_score": int,
                    "away_score": int
                }
            ],
            "bet": <Bet>
        }
    }

##### Notes

Only bets that the authenticated user is allowed to view
at this time will be retrieved.

The ```"bet"``` data entry will only be included if a specific ID
was provided.
