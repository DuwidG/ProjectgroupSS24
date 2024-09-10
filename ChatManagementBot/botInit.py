
import os, logging, json, com.ChatManagementBot.webexBot as webexBot
from webexteamsbot import TeamsBot


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


# Retrieve required details from environment variables
bot_email = os.getenv("WEBEX_BOT_EMAIL")
teams_token = os.getenv("WEBEX_BOT_TOKEN")
bot_url = os.getenv("WEBEX_BOT_URL")
bot_app_name = "UKB Food Bot"

approved_users = json.loads(os.environ['WEBEX_APPROVED_USERS'])

class Calls:
    def webexCall(self, incoming_msg):
        response = webexBot.main(incoming_msg)
        return response
    
calls = Calls()
      
# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    approved_users=approved_users,

)

bot.set_greeting(calls.webexCall)


if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)