# Food Bot Queries
|Question|Expectation|Response|
|--------|-----------|--------|
|What's for Lunch Today?|List of Items on Todays Menu|correct, ignored double entry|
|What can I eat tomorrow?|Understanding relative date, returning corresponding list |Incorrect, gives Menu for Thursday instead of Tuesday|
|What vegetarian options are there on Wednesday?|List of Items fitting criteria, or deniying availability|correct|
|What can i eat today if i don't want to spend more than 2 euros?|List of Items fitting criteria (day & price)|incorrect, forgets One Item|
|On which days can i eat currywurst?|Reply with List of Days, when Currywurst is available|correct|
|German Tests|||
|Was gibts heute?|List of Items on Todays Menu|correct|
|Was gibt es alles Montags, dass halal ist?|List of Items fitting criteria (diet & day)|incorrect, forgets One Item|
|Qué hay de almuerzo hoy?| List of Items on Todays Menu in spanish|correct|

---

# Chatroom Bot Queries
|Question|Expectation|Response|Function Call|
|--------|-----------|--------|-------------|
|Create a Room for me named Sprintkickoffmeeting|Create a Room, respond with confirmation and link|correct|correct|
|Can you invite duwid_test to the room Sprintkickoffmeeting|Invite duwid_test to room, and confirm|correct|correct|
|Can you invite daniel to the room "New Years"|Deny and give reason room|correct|correct|
|Can you invite "daniel" to the room "Sprintkickoffmeeting"|Deny and give reason name|correct|correct|
|(room exists) Delete the room Sprintkickoffmeeting|Delete the Room, respond with confirmation|correct|correct|
|(room doesn't exist) Delete the room Sprintkickoffmeeting|Deny and give reason room|correct|correct|
|German||||
|Erstelle einen Raum namens Montagsmeeting|Create a Room, respond with confirmation and link|correct|correct|
|Lösche den Raum namens Montagsmeeting|Delete the Room, respond with confirmation|correct|correct|
