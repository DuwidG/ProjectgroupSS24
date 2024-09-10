import time
import com.shared.ollama_requester as ollama
import MensaAPI as mensa
import logging
import json
from os import path
import rag

logger = logging.getLogger(__name__)

file_path = "com/FoodBot/data/menu.json"

outdateTime = 21600 # 6 hours

# uses markdown to format the text
def _prettify(menu : dict[str : mensa.MenuItem]):
    text = ""
    for day, daysMenu in menu.items():
        text += f"##Menu for {day}:\n\n"
        for item in daysMenu:
            if 'price' in item and item['price'] is not None:
                text += f"- **{item['name']} - {item['price']} available on {day}**\n"
            else:
                text += f"- **{item['name']} - ?,??€**\n"
            # Check if the item has any additional information
            if 'contains' in item and len(item['contains']) > 0:
                text += f"  - *Additional Information*: {', '.join(item['contains'])}\n"
            # Check if the item contains any additives
            if 'additives' in item and len(item['additives']) > 0:
                text += f"  - *Additives*: {', '.join(item['additives'])}\n"
            # Check if the item contains any allergens
            if 'allergens' in item and len(item['allergens']) > 0:
                text += f"  - *Allergens*: {', '.join(item['allergens'])}\n"
            text += "\n"
    if(menu == None):
        return "No menu available"
    return text

def _jsonify(menu: [mensa.MenuItem]):
    return json.dumps(menu, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

def writeToFile(Text):
    with open(file_path, "w", encoding='utf-8')as file:
        file.write(Text)
    return

def getFullWeeksMenu(forceUpdate : bool = False, asString : bool = False, pretty : bool = False):
    last_edit_time = time.time() - path.getmtime(file_path)
    # Update if local file is outdated or update is explicitly wanted
    if (last_edit_time > outdateTime or forceUpdate):
            fullweek = mensa.getWeeklyMenu()
            jsonMenu = _jsonify(fullweek)
            writeToFile(jsonMenu)
    else:
        logger.info(f"Menu file was updated less than {outdateTime/60/60} hours ago, using cached data.")

    with open(file_path, "r", encoding='utf-8') as file:
        file_contents = file.read()

    if pretty:
        return _prettify(json.loads(file_contents))
    elif not asString:
        return json.loads(file_contents)
    
    return file_contents


def main(incoming_msg, incoming_text : str = None):
    if(incoming_text is None):
        incoming_text = incoming_msg.text

    logger.info("FoodBot triggered with: \""+str(incoming_text)+ "\" by: <"+str(incoming_msg.personEmail)+ "> trough: "+str(incoming_msg.roomType))

    weeklyMenu = _prettify(getFullWeeksMenu())
    today = mensa.getWeekDay()

    rag_question = incoming_text.join(f" Today is {today}")

    formattedMenu = rag.getFormattedContext(menu_str=weeklyMenu, question=rag_question)

    ollamaAnswer = ollama.query_answer(message=incoming_text, system_prompt=
                                       f"You are an Assistant for the Menu at the Mensa of the Clinic \"Uniklinik Bonn\", Today is {today}, The Mensa is open during the weekdays, " 
                                       f"Only list additional Information like allergens and additives if the user asks for it, do not list them by default."
                                       f"You're answering the user in their language, which is probably not be english, you may need to translate, stay concise and to the point.",
                                       context=formattedMenu
                                       )
    return ollamaAnswer

def test():

    weeklyMenu = getFullWeeksMenu(pretty=True)

    question = "What can i eat thats vegetarian on Monday?"

    today = mensa.getWeekDay()

    formattedMenu = rag.getFormattedContext(menu_str=weeklyMenu, question=question)

    ollamaAnswer = ollama.query_answer(message=question, system_prompt=
                                       f"You are an Assistant for the Menu at the Mensa of the Clinic \"Uniklinik Bonn\", Today is {today}, The Mensa is only opened during the weekdays," 
                                       f"Only list additional Information like allergens and additives if the user asks for it, do not list them by default."
                                       f"Your answer has to be in the language of the user, you may need to translate, stay concise and to the point.",
                                       context=formattedMenu
                                       )

    return ollamaAnswer