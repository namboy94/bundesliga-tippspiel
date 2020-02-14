# bundesliga-tippspiel API

Bundesliga-Tippspiel offers a JSON API using GET, POST and PUT HTTP methods.

### Sending requests

To start off, we'll discuss how requests are sent.

##### Authorization

Authorization is handled using basic HTTP authentication headers.
The format is like this:

    "Authorization": "Basic <API Key>"
    
Some requests do not require authentication, those can simply be called.

You can aquire an API key by POSTing the username and password to
the [api_key](endpoints/api_key.md) endpoint. To check
if any given API key is valid, it's possible to use the
[authorize](endpoints/authorize.md) endpoint.

API keys stay valid for 30 days, after which they expire.

##### GET

GET requests need to add the query parameters in the URL.

Example:

    GET hk-tippspiel.com/api/v2/bets?username=me

##### POST/PUT

POST/PUT requests should be in JSON format, with the values associated
with the appropriate keys.

Examples:

    POST hk-tippspiel.com/api/v2/register
    
    //data:
    {
        "username": "me",
        "email": "me@example.com",
        "password": "hunter2",
        "password_repeat": "hunter2",
        "recaptcha_response": "..."
    }

    PUT hk-tippspiel.com/api/v2/bet
    
    // data:
    {
        "match_id": 1,
        "home_score": 2,
        "away_score": 1
    }

### Responses

The API will always respond with JSON.

If there were no errors processing the API request, the response will look
like this:

    {
        "status": "ok",
        "data": {...}
    }
    
Should an error occur while handling the API request, the response will look
like this:

    {
        "status": "error",
        "reason": "Reason for the error"
    }

### More details

For more details on the individual API endpoints, check out the following
documents:

Account Creation and Management:

* [api_key](endpoints/api_key.md)
* [authorize](endpoints/authorize.md)
* [register](endpoints/register.md)

Data Fetching:

* [leaderboard](endpoints/leaderboard.md)
* [bet](endpoints/bet-get.md)
* [goal](endpoints/goal.md)
* [match](endpoints/match.md)
* [player](endpoints/player.md)
* [team](endpoints/team.md)


Generating user-created content:

* [bet](endpoints/bet-put.md)
