from pydantic import BaseModel


class CharacterAtributtes(BaseModel):
    game: str | None = None
    name: str | None = None
    char_class: str | None = None
    race: str | None = None
    origin: str | None = None
    weapon: str | None = None
    god: str | None = None
    build: str | None = None


class AiResponse(BaseModel):
    game: str
    name: str
    char_class: str
    race: str
    origin: str
    weapon: str
    god: str
    build: str
    lore: str
    physical_characteristics: str
    personality_traits: str
    other_characteristics: str

    model_config = {'from_attributes': True}
