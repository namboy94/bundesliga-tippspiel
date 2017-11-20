# API Specification

All API responses are in JSON format.

Path: `hk-tippspiel.com/api/v1/` + endpoint

You can check if an API request was successful by checking the
"status" value of the response. The API request is only successful
if that value is set to "success". The cause of the failure can be determined
using the "cause" value of the response.

## Authentication

To generate an API key, use the [request_api_key](api/request_api_key.md)
endpoint. To check if an API key is valid, use the
[authorize](api/authorize.md) endpoint.

# Retrieving Match Information

To get matchday information, use the
[get_matches_for_matchday](api/get_matches_for_matchday.md) endpoint.
To retrieve a user's bets for a given matchday, use the
[get_user_bets_for_matchday](api/get_user_bets_for_matchday.md) endpoint.

# Placing bets

You can place bets using the [place_bets](api/place_bets.md) endpoint.