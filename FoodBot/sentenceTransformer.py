from sentence_transformers import SentenceTransformer, util

import numpy as np
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


model = SentenceTransformer("all-MiniLM-L6-v2")

tensor_cutoff = 0.4
tensor_closeRange = 0.0

command_bundle = [
                {"desc":"Create a new chatroom. Can you make a new group.", "command":"api.rooms.create()"},
                {"desc":"Erstelle einen neuen Chatraum. Kannst du einen neue Gruppe erstellen.", "command":"api.rooms.create()"},

                {"desc":"Delete the chatroom. Can you get rid of the group for me. ", "command":"api.rooms.delete(room.id)"},
                {"desc":"Lösche den Chatraum. Kannst du die Gruppe auflösen", "command":"api.rooms.delete(room.id)"},

                {"desc":"Get the food information from the cafe and mensa. Whats for lunch today and tomorrow. What is the cafeteria offering?","command": "foodCall"},
                {"desc":"Hole die Information über das essen in der Mensa und dem Cafe. Was gibt es heute und morgen zu essen. Was kann ich mir in der Mensa zu essen holen. Was gibts heute?","command": "foodCall"},

                {"desc":"Get the weather information","command": "api.weather().today"},
                {"desc":"Hole die Wetter informationen","command": "api.weather().today"}
                ]


# check if the highest tensor is below the defined cutoff
def _isLow(cos_sim):
    return cos_sim.max() < tensor_cutoff

# check if the highest tensor is close to the second highest tensor
def _isClose(cos_sim):
    alpha = 0.1
    sorted_cos_sim = np.sort(cos_sim, axis=1)
    return sorted_cos_sim[:,-1] - sorted_cos_sim[:,-2] < tensor_closeRange

# encode the commands into vectors and create a list only comprised of the commands
# should be a list of strings
def _encodeEmbedding(embedThis_list):
    command_list = []
    if(embedThis_list is command_bundle):
        for dict in command_bundle:
            command_list.append(dict["desc"])
        embeddings = model.encode(command_list)
    embeddings =  model.encode(embedThis_list)
    return embeddings

# find the text that is most similar to the input
def findCommand(input, detectThis = command_bundle):
    embedding = _encodeEmbedding(detectThis)
    # encode the input, compute similarity with all commands
    input_encoded = model.encode(input)
    cos_sim = util.cos_sim(input_encoded, embedding)

    # get the index with the highest similarity value
    c_idx = cos_sim.argmax(1)

    # exit if no good match with given commands
    if(_isLow(cos_sim)):
        logger.warn("WARN: Below cutoff: "+str(cos_sim.max()))
        return "No good match found. Please try again."
    
    if(_isClose(cos_sim)):
        logger.warn("WARN: Incoming message is an ambiguous match, therefore no action will be taken.")
        return "Multiple matches found. Please try again."

    target_command_dict = command_bundle[c_idx]

    return target_command_dict