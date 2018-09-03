# /leaderboard

This API endpoint allows fetching the current leaderboard data.

##### Methods

* GET

##### Authorization

Required

##### Parameters

None

##### Response

* **leaderboard:list**: A sorted list of tuples containing the leaderboard data

    {
        "status": "ok",
        "data": {
            "leaderboard": [
                (<User>, points),
                ...
            ]
        }
    }

##### Notes

The leaderboard is in the form of a list of tuples. The first element
represents the first position in the leaderboard.
