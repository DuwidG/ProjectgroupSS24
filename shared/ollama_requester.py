import os, logging
from ollama import Client
from ollama import ChatResponse

logger = logging.getLogger(__name__)

hostIP = os.getenv("OLLAMA_HOST")
client = Client(host=hostIP)
model = "mistral-nemo"
maxTokens =8000
temperature = 0.2

conversationLog = []

options = {
    'num_ctx' : maxTokens,
    'temperature' : temperature
    }


def _addContext(message : str, context : str):
    if context is not None:
        return f"Question:\n{message}\n\nContext:\n{context}"
    return message

def query(message : str, system_prompt : str = '', context : str = None, tools : str = None) -> ChatResponse:
    userMessage = _addContext(message, context)
    response = client.chat(tools=tools, model=model, options= options, messages=[
        {
            'role': 'system',
            'content': system_prompt,
        },
        {
            'role': 'user',
            'content': userMessage,
        },
    ])
    return response

def query_answer(message : str, system_prompt : str = '', context : str = ''):
    response = query(message, system_prompt, context)
    return response['message']['content']

def getEmbeddings(text):    
    response = client.embeddings(model='mistral', prompt=text)
    return response

def conversation(message : str, tools : str = None, system_prompt : str = None, restartConvo : bool = False) -> ChatResponse:
    # do this in order to restart the conversation
    if restartConvo:
        global conversationLog
        conversationLog = []
    # always do: 
    if(len(conversationLog) == 0):
        conversationLog.append({"role": "system", "content": system_prompt})
    
    conversationLog.append({"role": "user", "content": message})
    logger.info(f"TO LLM: {message}")
    response : ChatResponse=  client.chat(tools=tools, model=model,options=options, messages=conversationLog)
    conversationLog.append({"role": "assistant", "content": response["message"]['content']})
    logger.info(f"FROM LLM: {response}")

    return response
