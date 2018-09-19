# /email_reminder (GET)

This API endpoint allows a user to retrieve their own
reminder settings. For information on setting a reminder, consult the
[email_reminder (PUT))](email-reminder-put.md) document.

##### Methods

* GET

##### Authorization

Required

##### Parameters

No parameters supported

Example:

    GET /api/v2/email_reminder

##### Response

* **reminder:Reminder|null**: The user's reminder data
  * **id:int**: The ID of the reminder
  * **user_id:int**: The ID of the user that set this reminder
  * **user:<User>**: The user that set this reminder
  * **reminder_time:int**: The amount of time before a match at which the 
                           reminder will be triggered in seconds
  * **last_reminder:str**: The time at which the reminder was last triggered


    {
        "status": "ok",
        "data": {
            "email_reminder": {
                "id": int,
                "user_id": int,
                "user": <User>,
                "reminder_time: int,
                "last_reminder": str
            }
        }
    }
