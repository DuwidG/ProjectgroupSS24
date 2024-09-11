# ChatManagementBot Documentation

## Overview
ChatManagementBot is a Webex Teams bot that manages Webex rooms using natural language interactions. It utilizes the Webex Teams API and an AI model (Ollama) to interpret user requests and perform actions.

## Components

### 1. botInit.py
- Initializes the Webex Teams bot
- Sets up environment variables and logging
- Creates a TeamsBot instance with approved users

### 2. webexBot.py
- Main logic for processing user messages
- Defines available tools (functions) for room management
- Uses Ollama for natural language processing
- Handles function calls based on AI model output

### 3. webexFunctions.py
- Implements Webex API calls
- Functions include:
  - listRooms(): List rooms the user is part of
  - createRoom(title): Create a new Webex room
  - removeRoom(title): Delete an existing Webex room
  - invitePersonToRoom(displayName, roomTitle, isModerator): Invite a person to a room

## Key Features
- Natural language interaction for Webex room management
- Creation and deletion of Webex rooms
- Inviting users to rooms
- Error handling for insufficient permissions or non-existent rooms/users

## Usage
Users can interact with the bot using natural language to perform Webex room management tasks. The bot interprets requests, calls appropriate functions, and provides user-friendly responses.

## Notes
- The bot uses environment variables for configuration
- Only approved users can interact with the bot
- The bot runs on port 5000 by default
