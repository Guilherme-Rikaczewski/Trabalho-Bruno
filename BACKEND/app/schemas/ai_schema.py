from enum import Enum
import unicodedata

from pydantic import BaseModel, field_validator


def _normalize_enum_value(value, prefix: str):
    if value is None or isinstance(value, Enum):
        return value

    normalized = unicodedata.normalize("NFKD", str(value))
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower().strip().replace(" ", "_").replace("-", "_")

    while "__" in normalized:
        normalized = normalized.replace("__", "_")

    if not normalized.startswith(prefix):
        normalized = f"{prefix}{normalized}"

    return normalized


class AiRole(str, Enum):
    TECHNICAL = "modo_tecnico"
    SUMMARIZED = "modo_resumido"
    TEACHER = "modo_professor"
    DETAILED = "modo_detalhado"
    TECH_SUPPORT = "modo_suporte_tecnico"


class PromptType(str, Enum):
    SIMPLE = "prompt_simples"
    STRUCTURED = "prompt_estruturado"
    SPECIALIZED = "prompt_especializado"


class CharacterAtributtes(BaseModel):
    game: str | None = None
    name: str | None = None
    char_class: str | None = None
    race: str | None = None
    origin: str | None = None
    weapon: str | None = None
    god: str | None = None
    build: str | None = None
    ai_role: AiRole = AiRole.DETAILED
    prompt_type: PromptType = PromptType.STRUCTURED

    @field_validator("ai_role", mode="before")
    @classmethod
    def normalize_ai_role(cls, value):
        return _normalize_enum_value(value, "modo_")

    @field_validator("prompt_type", mode="before")
    @classmethod
    def normalize_prompt_type(cls, value):
        return _normalize_enum_value(value, "prompt_")


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
