from enum import Enum
import uuid
from pydantic import BaseModel
from typing import Annotated, TypeAlias
from fastapi import FastAPI, Query

class CharacterType(str, Enum):
    PLAYABLE = "playable"
    KEY_NPC = "key_npc"
    RANDOM_NPC = "random_npc"
    ENEMY = "enemy"

class CharacterRace(str, Enum):
    HUMAN = "human"
    DROW = "drow"
    ORC = "orc"
    #add more

class CharacterClass(str, Enum):
    FIGHTER = "fighter"
    ROGUE = "rogue"
    BARBARIAN = "barbarian"
    #add more

class Character(BaseModel):
    type: CharacterType
    name: str
    race: CharacterRace
    classes: list[CharacterClass] | None
    level: int | None
    description: str | None
    appearance: str | None

characters = {
    12345: {
        "id": 12345,
        "type": CharacterType.PLAYABLE,
        "race": CharacterRace.HUMAN,
        "classes": [CharacterClass.FIGHTER],
        "name": "Robert Salvatore"
    },
    34567: {
        "id": 34567,
        "type": CharacterType.PLAYABLE,
        "race": CharacterRace.ORC,
        "classes": [CharacterClass.BARBARIAN],
        "name": "Jorjik Shmakov"
    }
}

app = FastAPI()

@app.get("/")
def root():
    return { "message": "Hello World!" }

@app.get("/characters")
def get_characters(type: CharacterType | None = None, skip: int = 0, limit: int | None = None):
    if not type:
        return characters
    match type:
        case CharacterType.PLAYABLE:
            return { "message": "Playable characters list endpoint" }
        case CharacterType.KEY_NPC:
            return { "message": "Key NPCs list endpoint" }
        case CharacterType.RANDOM_NPC:
            return { "message": "Random NPCs list endpoint" }
        case CharacterType.ENEMY:
            return { "message": "Enemies list endpoint" }
    # TODO: make up some db fake and return a slice from it

@app.get("/characters/{char_id}")
def get_characted_by_id(char_id: str):
    return { "id": char_id }

@app.post("/characters")
def create_character(character: Character):
    id = uuid.uuid4().int
    character_dict = character.model_dump()
    character_dict.update({ "id": id })
    characters.update({ id: character_dict })
    return character_dict

@app.put("/characters/{char_id}")
def update_character(char_id: int, character: Character):
    character_dict = character.model_dump()
    character_dict.update({ "id" : char_id })
    characters[char_id] = character_dict
    return character_dict

### messaging

type MessageAuthor = Annotated[str, Query(max_length=16)]
type MessageText = Annotated[str, Query(max_length=80)]

# for Python <3.12
# MessageAuthor: TypeAlias = Annotated[str, Query(max_length=16)]
# MessageText: TypeAlias = Annotated[str, Query(max_length=80)]

class Message(BaseModel):
    author: MessageAuthor | None = None
    text: MessageText
    
messages: list[Message] = []

@app.get("/messages")
def get_messages_by_author(author: MessageAuthor | None = None):
    if not author:
        return messages
    return list(filter(lambda x: x.author == author, messages))

@app.post("/messages")
def post_message(message: Message):
    print(messages)
    messages.append(message)
    return message

@app.get("/test")
def get_test_author(author: Annotated[MessageAuthor, Query(alias="who")]):
    return { "message": author }