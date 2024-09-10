Bot Setup Documentation:

1. Import Dependencies:
   - Import necessary modules, including os, logging, json, and custom modules.
   - Import TeamsBot from webexteamsbot.

2. Configure Logging:
   - Set up basic logging configuration.

3. Environment Variables:
   - Retrieve bot details from environment variables:
     - WEBEX_BOT_EMAIL
     - WEBEX_BOT_TOKEN
     - WEBEX_BOT_URL
   - Set bot_app_name (e.g., "UKB Food Bot").
   - Load approved users from WEBEX_APPROVED_USERS environment variable.

4. Create a Calls Class:
   - Define a class Calls with methods to handle different types of incoming messages.
   - Example methods: webexCall, foodCall.

5. Instantiate Bot:
   - Create a TeamsBot object with the following parameters:
     - bot_app_name
     - teams_bot_token
     - teams_bot_url
     - teams_bot_email
     - approved_users

6. Set Bot Greeting:
   - Use bot.set_greeting() to set the main message handler.
   - Pass a method from the Calls class as the greeting function.

7. Additional Setup (optional):
   - Perform any necessary initializations (e.g., updating menu files).

8. Run the Bot:
   - Use if __name__ == "__main__": to ensure the bot only runs when the script is executed directly.
   - Call bot.run() with host and port parameters to start the bot.

This structure allows for easy customization of bot behavior by modifying the Calls class methods and adjusting the greeting function as needed.