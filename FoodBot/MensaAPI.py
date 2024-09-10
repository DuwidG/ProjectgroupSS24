import time
from datetime import datetime
import logging
import seleniumScraper as scraper


logger = logging.getLogger(__name__)

timeout: float = 900

savedMenu = {"monday": [], "tuesday": [] ,"wednesday": [], "thursday": [] , "friday": []}
weekDaysEN = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]



class MenuItem:
    name : str
    price : float

    contains : str = []
    additives : str = []
    allergens : str = []
    def __init__(self, name: str, price: float = None, day : str = None):
        self.name = name
        self.price = price

    
    def setMacros(self, description: str):
        entry = "contains"
        macros = description.split("  ")
        macroDict = {"contains": [], "additives": [], "allergens": []}
        for item in macros:
            # remove leading whitespaces
            item = item.lstrip()
            # check if the item is a keyword
            if(item == "ZUSATZ"):
                entry = "additives"
            elif(item == "ALLERGEN"):
                entry = "allergens"
            else:
                # add the item to the current entry
                macroDict[entry].append(item)
        self.contains = macroDict["contains"]
        self.additives = macroDict["additives"]
        self.allergens = macroDict["allergens"]
        return 


# Updates the menu for the specified day by scraping the meal descriptions from the website
def _updateMenuForDay(day: int):
    menuForToday = []
    weekDays = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]

    menuItems, menuPrices, menuDescription = scraper.scrape(day)

    for i in range(len(menuItems)):
        try:
            dish = MenuItem(menuItems[i], menuPrices[i], weekDays[day])
        except:
            dish = MenuItem(menuItems[i], None, weekDays[day])
            logger.warn(f"WARN: No price found for {dish.name}")
            
        try:
            dish.setMacros(menuDescription[i])
        except:
            logger.warn(f"WARN: No additional information found for {dish.name}")
        menuForToday.append(dish)

    return menuForToday


# Updates the full menu by scraping meal descriptions for each day of the week and returns it
def getWeeklyMenu():
    for dayIterator in range(0,5):
        logger.info(f"Scraping menu for {weekDaysEN[dayIterator]}")
        savedMenu[weekDaysEN[dayIterator]] = _updateMenuForDay(dayIterator)
    return savedMenu

def getWeekDay(dayIterator: int = datetime.today().weekday()):
    return weekDaysEN[dayIterator]


# Returns the mensa menu for the specified day of the current week, if not specified current day
def getMenuForToday(dayIterator: int = datetime.today().weekday()):
    if(dayIterator > 4):
        return None
    
    return savedMenu[weekDaysEN[dayIterator]]