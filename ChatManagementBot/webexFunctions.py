import logging
from webexteamssdk import WebexTeamsAPI
from webexteamssdk import Room, Person, RoomMeetingInfo, Membership, ApiError

logger = logging.getLogger("WEBEX API CALLS")

api = WebexTeamsAPI()

user : Person= api.people.me()

def _findRoom(title : str) -> Room:
    rooms = api.rooms.list()
    for room in rooms:
        if(room.title == title):
                return room
    return None

def _findPerson(displayName : str) -> Person:
    people = api.people.list()
    person : Person
    for person in people:
        if(person.displayName == displayName):
            return person
    return None



def listRooms() -> str:
    roomlist = []
    myRooms = api.rooms.list()
    room : Room
    for room in myRooms:
        roomlist.append(room.title)
    logger.debug(f"List of rooms user is part of\n{roomlist}")
    return f"This is the list of rooms the user is part of: {roomlist}"

def createRoom(title : str) -> str:
    try:
        room : Room= api.rooms.create(title)
    except ApiError:
        logger.exception("The Room could not be created!")
    roomInfo : RoomMeetingInfo = api.rooms.get_meeting_info(room.id)
    logger.info(f"The room has been successfully created: {roomInfo}")
    return f"The Webex Room has been created, with the title {room.title} and the meeting link: {roomInfo.meetingLink}"

def removeRoom(title : str) -> str:
    room = _findRoom(title)
    if(room is not None):
        if(room.creatorId != user.id):
            logger.warn("Insufficent Permission")
            return f"You don't have the rights to delete the room {title}, you are not the creator of it. You can leave it manually if you want to"

        api.rooms.delete(roomId=room.id)
        logger.debug(f"This room has been deleted:\n{room}")
        return f"Room with title \"{title}\" has been removed."
    else:
        logger.warn("No room found")
        return f"No room was found with the title \"{title}\". Perhaps there is a typo?"
    

def invitePersonToRoom(displayName : str, roomTitle : str, isModerator : bool = False) -> str:
    # get room and person by names
    room = _findRoom(roomTitle)
    person = _findPerson(displayName)

    if(room is None):
        return f"No room was found with the title \"{roomTitle}\". Perhaps there is a typo?"
    if(person is None):
        return f"No Person was found with the nickname \"{displayName}\". Perhaps there is a typo?"
    
    try:
        newMembership : Membership=  api.memberships.create(roomId=room.id,personId=person.id, isModerator=isModerator)
    except ApiError:
        logger.error(f"Failed to create a new Membership")
        return f"You seem to not have the rights to invite {displayName} to the room {roomTitle}."
    
    logger.debug(f"New Membership created: \n{newMembership}")
    invitedRoom : Room = api.rooms.get(newMembership.roomId)
    return f"You have successfully added {newMembership.personDisplayName}, with email {newMembership.personEmail} into the room {invitedRoom.title}"