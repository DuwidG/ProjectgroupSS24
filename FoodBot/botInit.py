import os , logging, json
import com.FoodBot.foodBot as food

from webexteamsbot import TeamsBot

logger = logging.getLogger(__name__)


# Retrieve required details from environment variables
bot_email = os.getenv("WEBEX_BOT_EMAIL")
teams_token = os.getenv("WEBEX_BOT_TOKEN")
bot_url = os.getenv("WEBEX_BOT_URL")
bot_app_name = "UKB Food Bot"

approved_users = json.loads(os.environ['WEBEX_APPROVED_USERS'])

      
# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    approved_users=approved_users,
)


def _removeMention(text : str):
    if text.startswith("Uniklinik"):
        return text[len("Uniklinik"):]

# Be able to have different functions as answers
class Calls:
    def foodCall(self, incoming_msg):

        incoming_text = _removeMention(incoming_msg.text)
        food_data = food.main(incoming_msg, incoming_text)

        return str(food_data)
    

    
# the different calls are stored here, so getattr() can invoke them
calls = Calls()


#Only use as Food Bot:
bot.set_greeting(calls.foodCall)


if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)