# /match

This API endpoint allows fetching goal data.

##### Methods

* GET

##### Authorization

Required

##### Parameters

The parameters are all optional and act as filters.

* **matchday:int**: Only returns matches from the specified matchday
                    If set to -1, will use the current matchday.
* **team_id:int**: Only returns matches in which the specified team
                   took part in.

To retrieve an element with a specific ID, append /<ID> to the URL.

Examples:

    GET /api/v2/match            # All matches
    GET /api/v2/match/1          # Match with ID 1
    GET /api/v2/match?matchday=1 # All matches from matchday 1

##### Response

* **matches:list**: A list of matches
  * **id:int**: The ID of the match
  * **home_team_id:int**: The ID of the home team
  * **away_team_id:int**: The ID of the away team
  * **home_team:<Team>**: The home team
  * **away_team:<Team>**: The away team
  * **matchday:int**: On which matchday this match was held
  * **home_current_score:int**: The current score of the home team
  * **away_current_score:int**: The current score of the away team
  * **home_ht_score:int**: The home team's score at half time
  * **away_ht_score:int**: The away team's score at half time
  * **home_ft_score:int**: The home team's score at full time
  * **away_ft_score:int**: The away team's score at full time
  * **kickoff:str**: The kickoff time in the format ```YYYY-MM-DD:HH-mm-ss```
  * **started: bool**: Indicated whether or not the match has started
  * **finished: bool**: Indicated whether or not the match has ended
* **match:<Match>**: A single match, only available when specific ID was provided


    {
        "status": "ok",
        "data": {
            "matches": [
                {
                    "id": int,
                    "home_team_id": int,
                    "away_team_id": int,
                    "home_team": <Team>,
                    "away_team": <Team>,
                    "matchday": int,
                    "home_current_score": int,
                    "away_current_score": int,
                    "home_ht_score": int,
                    "away_ht_score": int,
                    "home_ft_score": int,
                    "away_ft_score": int,
                    "kickoff": str,
                    "started": bool,
                    "finished": bool
                }
            ],
            "match": <Match>
        }
    }

##### Notes

The ```"match"``` data entry will only be included if a specific ID
was provided.
