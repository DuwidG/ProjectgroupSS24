from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

Options = Options()
Options.add_argument("--headless")

# Constructs the URL for the specified day's menu page
def _buildURL(day: int):
    weekDays = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]
    baseURL = "https://www.imensa.de/bonn/venusberg-bistro/"

    return baseURL + weekDays[day] + ".html"

def _extractText(elements):
    list = []
    for item in elements:
        list.append(item.text)
    return list

def scrape(day: int):
    driver = webdriver.Firefox(options=Options)
    driver.get(_buildURL(day))
    # Wait for the page to load
    driver.implicitly_wait(2)
    # Get the menu items
    menuItems = _extractText(driver.find_elements(By.CLASS_NAME, 'aw-meal-description'))
    # Get the menu prices
    menuPrices = _extractText(driver.find_elements(By.CLASS_NAME, 'aw-meal-price'))
    # Get the menu descriptions
    menuDescription = _extractText(driver.find_elements(By.CLASS_NAME, 'aw-meal-attributes'))

    driver.quit()

    return menuItems, menuPrices, menuDescription