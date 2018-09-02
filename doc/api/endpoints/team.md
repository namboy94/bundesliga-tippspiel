# /team

This API endpoint allows fetching team data.

##### Methods

* GET

##### Authorization

Required

##### Parameters

To retrieve an element with a specific ID, append /<ID> to the URL.

Examples:

    GET /api/v2/team    # All teams
    GET /api/v2/team/1  # Team with ID 1

##### Response

* **teams:list**: A list of teams
  * **id:int**: The ID of the team
  * **name:str**: The full name of the team
  * **short_name:str**: A shortened name of the team, maximum 16 characters
  * **abbreviation:str**: A 3-character abbreviation of the team's name
  * **icon_svg:str**: A URL path to an icon file of the team's logo in SVG format
  * **icon_png:str**: A URL path to an icon file of the team's logo in PNG format
* **team:<Team>**: A single team, only available when specific ID was provided


    {
        "status": "ok",
        "data": {
            "teams": [
                {
                    "id": int,
                    "name": str,
                    "short_name": str,
                    "abbreviation": str,
                    "icon_svg": str,
                    "icon_png": str
                }
            ],
            "team": <Team>
        }
    }

##### Notes

The ```"team"``` data entry will only be included if a specific ID
was provided.
