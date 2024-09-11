# FoodBot Documentation

FoodBot is a Webex Teams bot designed to provide information about the menu at the Uniklinik Bonn Mensa (cafeteria).

## Main Components

1. **botInit.py**: Initializes the bot and sets up the main functionality.
2. **foodBot.py**: Contains the core logic for handling menu-related queries.
3. **MensaAPI.py**: Manages menu data retrieval and storage.
4. **rag.py**: Implements Retrieval-Augmented Generation for context-aware responses.
5. **seleniumScraper.py**: Scrapes menu information from the Mensa website.

## Key Features

- Retrieves and stores weekly menu data
- Responds to user queries about menu items
- Supports natural language processing for menu-related questions
- Provides information on vegetarian options, allergens, and additives when requested

## Implementation Details

### Bot Initialization (botInit.py)
- Sets up the TeamsBot instance
- Configures approved users and bot credentials
- Defines the main message handling function (foodCall)

### Core Logic (foodBot.py)
- Manages menu data updates and caching
- Processes user queries using RAG and Ollama for natural language understanding
- Formats menu data for display

### Menu Data Management (MensaAPI.py)
- Defines MenuItem class for storing dish information
- Implements functions to retrieve and update menu data
- Handles menu scraping for each day of the week

### Retrieval-Augmented Generation (rag.py)
- Uses Langchain and Ollama for embedding and retrieval
- Formats context based on user queries for improved responses

### Web Scraping (seleniumScraper.py)
- Uses Selenium with Firefox in headless mode to scrape menu data
- Extracts menu items, prices, and additional information

## Usage

The bot responds to user queries in Webex Teams, providing information about the current week's menu, specific dishes, and dietary options. It uses natural language processing to understand and respond to a variety of menu-related questions.

## Dependencies

- webexteamsbot
- Selenium
- Langchain
- Ollama
- Chroma

## Note

Ensure all required environment variables (WEBEX_BOT_EMAIL, WEBEX_BOT_TOKEN, WEBEX_BOT_URL, WEBEX_APPROVED_USERS) are set before running the bot.
