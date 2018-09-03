# /player

This API endpoint allows fetching player data.

##### Methods

* GET

##### Authorization

Required

##### Parameters

The parameters are all optional and act as filters.

* **team_id:int**: Only returns players belonging to the specified team.

To retrieve an element with a specific ID, append /<ID> to the URL.

Examples:

    GET /api/v2/player           # All players
    GET /api/v2/player/1         # Player with ID 1
    GET /api/v2/player?team_id=1 # All players from team 1

##### Response

* **players:list**: A list of players
  * **id:int**: The ID of the player
  * **team_id:int**: The ID of the player's team
  * **team:<Team>**: The player's team
  * **name:str**: The player's name
* **player:<Player>**: A single player, only available when specific ID was provided


    {
        "status": "ok",
        "data": {
            "players": [
                {
                    "id": int,
                    "team_id": int,
                    "team": <Team>,
                    "name": str
                }
            ],
            "player": <Player>
        }
    }

##### Notes

The ```"player"``` data entry will only be included if a specific ID
was provided.
