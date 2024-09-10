# Ukb-Bots - Proof of Concept

## Project Description
Ukb-Bots is a proof of concept that includes two separate Webex Bots developed in Python. The first bot provides information about the weekly Mensa menu, and the second bot manages your Webex rooms. Both bots receive commands in natural language, which are processed using Mistral-NeMo on the Ollama platform.

## Installation Instructions

### Prerequisites
1. **Register a Bot with Webex:**
   - Go to [Webex for Developers](https://developer.webex.com) and register your bot to obtain the necessary credentials.
   - On the same website get your own api token(valid for 12h), so webex rooms can be created and deleted in your name.
   - The Bots require access to an **Ollama** API running Mistral-NeMo. Ensure that this is properly set up.
   - You need **ngrok** to host the webex Bots, so that webex can access them.

2. **Required Python Modules:**
   - Install the following Python modules using `pip`:
     - `webexteamsbot` (for the base Webex bot functionality)
     - `webexteamssdk` (for Webex API access)
     - `langchain` (for RAG approach)
     - `selenium` (for web scraping)
     - `sentence-transformers` (for string matching via vectors)

   ```bash
   pip install webexteamsbot webexteamssdk langchain selenium sentence-transformers
   ```

## Usage Instructions
The bots are designed to communicate in natural language due to their integration with Ollama. They can:
- Provide detailed information on the weekly Mensa menu.
- Manage your Webex rooms based on the commands received.

### Running the Bots
Make sure ngrok http is up and running on port 5000. You need to set the url as the WEBEX_BOT_URL env
Before executing the Python scripts, ensure that the following environment variables are set:

```bash
export PYTHONPATH=<your-python-path>
export WEBEX_BOT_EMAIL=<your-webex-bot-email>
export WEBEX_BOT_TOKEN=<your-webex-bot-token>
export WEBEX_BOT_URL=<your-ngrok-url>
export WEBEX_APPROVED_USERS=<approved-users-list>
export WEBEX_TEAMS_ACCESS_TOKEN=<your-personal-webex-api-token>
export OLLAMA_HOST=<ollama-api-host>
export TOKENIZERS_PARALLELISM=true  # Optional
```

## Features
- **Natural Language Processing:** The bots can interpret and execute commands in natural language.
- **Mensa Menu Information:** One bot provides up-to-date information on the weekly Mensa menu.
- **Webex Room Management:** The other bot can manage your Webex rooms based on the commands given.

## Contributing
This project is a student project for UKB and the University of Bonn, and no contributions are currently accepted.

## Credits
Special thanks to Edwin / Yang Yifan for supervising the project.