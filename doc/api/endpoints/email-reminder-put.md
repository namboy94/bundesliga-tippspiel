# /email_reminder (PUT)

This API endpoint allows a user to set an email reminder.
For information on retrieving previously set reminders, consult the
[email_reminder (GET))](email-reminder-get.md) document.

##### Methods

* PUT

##### Authorization

Required

##### Parameters

* **hours:int**: The amount of hours that the reminder should trigger
                 before the next unbet match. Must be between 1 and 48.
* **active:bool**: Specifies whether or not the reminder should be set as
                   active or not

**Examples**:

This will set a reminder that triggers 12 hours before the match starts:


    {
        "hours": 12,
        "active": true
    }

##### Response

    {
        "status": "ok",
        "data": {}
    }
