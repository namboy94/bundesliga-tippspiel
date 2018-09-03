# /bet

This API endpoint allows fetching goal data.

##### Methods

* GET

##### Authorization

Required

##### Parameters

The parameters are all optional and act as filters.

* **matchday:int**: Only returns goals from the specified matchday
* **match_id:int**: Only returns goals for the specified match
* **player_id:int**: Only returns goals scored by the specified player
* **team_id:int**: Only returns goals scored by player of the specified team


To retrieve an element with a specific ID, append /<ID> to the URL.

Examples:

    GET /api/v2/goal                         # All goals
    GET /api/v2/goal/1                       # Goal with ID 1
    GET /api/v2/goal?player_id=3&match_id=4  # Goals scored by player 3 in match 4

##### Response

* **goals:list**: A list of goals
  * **id:int**: The ID of the goal
  * **player_id:int**: The ID of the player that scored this goal
  * **player:<Player>**: The user that scored this goal
  * **match_id:int**: The ID of the match that this goal was scored in
  * **match:<Match>**: The match that this goal was scored in
  * **minute:int**: The minute in which this goal was scored
  * **minute_et:int**: The minute of extra time the goal was scored
  * **home_score:int**: The score of the home team after the goal was scored
  * **away_score:int**: The score of the away team after the goal was scored
  * **own_goal:bool**: Indicates whether or not the goal was an own goal
  * **penalty:bool**: Indicates whether or not the goal was a penalty
* **goal:<Goal>**: A single goal, only available when specific ID was provided


    {
        "status": "ok",
        "data": {
            "goals": [
                {
                    "id": int,
                    "match_id": int,
                    "match": <Match>,
                    "player_id": int,
                    "player": <Player>,
                    "minute": int,
                    "minute_et": int,
                    "home_score": int,
                    "away_score": int,
                    "own_goal": bool,
                    "penalty": bool
                }
            ],
            "goal": <Goal>
        }
    }

##### Notes

The ```"goal"``` data entry will only be included if a specific ID
was provided.
