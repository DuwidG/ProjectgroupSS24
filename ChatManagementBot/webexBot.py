import com.ChatManagementBot.webexFunctions as webexFunctions, json, logging
import com.shared.ollama_requester as ollamaReq
from ollama import ChatResponse
from webexteamssdk import Room

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

tools = [
    {
        "type": "function",
        "function": {
            "name": "createRoom",
            "description": "Create a Webex Room",
            "parameters": {
                'type': 'object',
                'properties': {
                    'title': {
                    'type': 'string',
                    'description': 'The title of the room create',
            },
          },
          'required': ['title'],
        },
        },
    },{
        "type": "function",
        "function": {
            "name": "removeRoom",
            "description": "Remove or Delete an existing Webex Room",
            "parameters": {
                'type': 'object',
                'properties': {
                    'title': {
                    'type': 'string',
                    'description': 'The title of the room to delete',
            },
          },
          'required': ['title'],
        },
        },
    },{
        "type": "function",
        "function": {
            "name": "invitePersonToRoom",
            "description": "Invite a Person to a Webex Room",
            "parameters": {
                'type': 'object',
                'properties': {
                    'displayName': {
                    'type': 'string',
                    'description': 'The displayName of the Person to invite',
                },
                    'roomTitle': {
                    'type': 'string',
                    'description': 'The title of the room to invite into',
            },
                    'isModerator': {
                    'type': 'bool',
                    'description': 'Whether or not the invited Person should have Moderator rights',
            },
          },
          'required': ['displayName','roomTitle'],
        },
        },
    }
]

systemPrompt = "You are a Webex Room Manager, who has access to some Webex API endpoints, "+ \
                "to the User you talk in their native language and appear natural with your answers, " + \
                "rephrase function returns and do not let them know you are making function calls, as if they are natural to you. " + \
                "You can only use the tools i am giving to you, nothing else concerning webex." + \
                "Do not Hallucinate"
functionLog = []
isHallucinating = False


namesToFuncs = {
    "createRoom" : webexFunctions.createRoom,
    "removeRoom" : webexFunctions.removeRoom,
    "invitePersonToRoom" : webexFunctions.invitePersonToRoom
}

def _hasTools(ollamaResponse: ChatResponse) -> bool:
    return 'tool_calls' in ollamaResponse['message']


def _useTools(ollamaResponse: ChatResponse):
    messages = []
    # Extract tool_calls
    tool_calls = ollamaResponse['message']['tool_calls']
    for tool_call in tool_calls:
        function = tool_call["function"]
        if(function["name"] in namesToFuncs):
            arguments = function["arguments"]
            result = namesToFuncs[function["name"]](**arguments)
            functionLog.append(function['name'])
            logOfFuncCall = f"Function {function['name']} called. Result: \n{result}" + \
                            f"\n Please relay the important information to the user"
            return logOfFuncCall
    return

def main(incoming_msg = None, message : str = None):
    logger.info(f"Incoming message: {incoming_msg}")
    global isHallucinating
    restart = False
    if(incoming_msg is not None):
        message = incoming_msg.text
    if(incoming_msg.text == "restart"):
        restart = True
    response : ChatResponse = ollamaReq.conversation(message=message, tools=tools, system_prompt=systemPrompt, restartConvo=isHallucinating or restart)
    if(type(response) is dict and response["message"]["content"].startswith("[TOOL")):
        if(restart):
            return "Okay, I'll try to reevaluate what you're saying, **please try again!**"
        logger.fatal("LLM starts to hallucinate")
        isHallucinating = True
        return "I'm Sorry, but something has gone wrong, **please try again!**"

    if _hasTools(response):
        messageToLLM = _useTools(response)
        logger.info(messageToLLM)
        response = ollamaReq.conversation(message=messageToLLM, system_prompt=systemPrompt) # Calling LLM with response from function
        
    else:
        logger.info("Response has no tools")


    
    return response["message"]["content"]

def test():
    return print(main(message="Create a room for me named planning"))

# TODO: creating rooms with seperate messages doesnt work, assisstant says it called the func, but doesnt actually do it
# All api calls are made with my key, therefore rooms can only be created in my name