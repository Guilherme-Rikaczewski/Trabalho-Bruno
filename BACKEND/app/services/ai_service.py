import ast
import json
import os
import re
import unicodedata

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
_llm = None

DEFAULT_VALUE = "Nao especificado"
RESPONSE_FIELDS = (
    "game",
    "name",
    "char_class",
    "race",
    "origin",
    "weapon",
    "god",
    "build",
    "lore",
    "physical_characteristics",
    "personality_traits",
    "other_characteristics",
)

ROLE_PROMPTS = {
    "modo_tecnico": (
        "Modo tecnico: seja objetivo, consistente com regras de RPG e use termos "
        "claros de classe, raca, origem e funcao do personagem."
    ),
    "modo_resumido": (
        "Modo resumido: produza textos curtos, diretos e sem floreios, mantendo "
        "todas as chaves obrigatorias preenchidas."
    ),
    "modo_professor": (
        "Modo professor: escreva de forma didatica, explicando a fantasia do "
        "personagem com linguagem facil de entender para jogadores iniciantes."
    ),
    "modo_detalhado": (
        "Modo detalhado: crie uma descricao rica, coerente e imersiva, com lore, "
        "aparencia e personalidade bem desenvolvidas."
    ),
    "modo_suporte_tecnico": (
        "Modo suporte tecnico: priorize respostas padronizadas, previsiveis e "
        "faceis de validar por uma API, sem sair do formato solicitado."
    ),
}

PROMPT_TYPES = {
    "prompt_simples": (
        "Prompt simples: crie um personagem medieval de RPG usando os atributos "
        "informados pelo usuario."
    ),
    "prompt_estruturado": (
        "Prompt estruturado: siga esta ordem: 1) validar os atributos recebidos; "
        "2) completar lacunas de forma coerente; 3) criar lore, aparencia, "
        "personalidade e outras caracteristicas; 4) retornar apenas o JSON final."
    ),
    "prompt_especializado": (
        "Prompt especializado: atue como game designer e mestre de RPG medieval. "
        "Crie um personagem pronto para campanha, com escolhas coerentes entre "
        "sistema, classe, raca, origem, arma, divindade e build."
    ),
}

BASE_PROMPT = """
Voce e uma IA especialista em criacao de personagens de RPG medieval.
{role_prompt}
{prompt_type}

Regras de consumo e resposta da API:
- Responda somente com um objeto JSON valido.
- Use aspas duplas em todas as chaves e valores.
- Nao use markdown, comentarios, texto antes ou depois do JSON.
- Nao invente chaves extras.
- Todas as chaves obrigatorias devem existir e conter texto.

Formato obrigatorio:
{{
  "game": "text",
  "name": "text",
  "char_class": "text",
  "race": "text",
  "origin": "text",
  "weapon": "text",
  "god": "text",
  "build": "text",
  "lore": "text",
  "physical_characteristics": "text",
  "personality_traits": "text",
  "other_characteristics": "text"
}}

Atributos recebidos:
- Sistema de jogo: {game}
- Nome: {name}
- Classe: {char_class}
- Raca: {race}
- Origem: {origin}
- Arma favorita: {weapon}
- Divindade: {god}
- Build: {build}
"""


def _get_llm():
    global _llm
    if _llm is None:
        if not api_key:
            raise Exception("GEMINI_API_KEY not configured")

        _llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=api_key,
            temperature=0.6,
        )

    return _llm


def _normalize_attributes(atributtes: dict) -> dict:
    normalized = atributtes.copy()
    for key, value in normalized.items():
        if value is None or value == "":
            normalized[key] = DEFAULT_VALUE

    normalized["ai_role"] = _normalize_option(
        normalized.get("ai_role", "modo_detalhado"),
        "modo_",
    )
    normalized["prompt_type"] = _normalize_option(
        normalized.get("prompt_type", "prompt_estruturado"),
        "prompt_",
    )
    return normalized


def _normalize_option(value, prefix: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(value))
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower().strip().replace(" ", "_").replace("-", "_")

    while "__" in normalized:
        normalized = normalized.replace("__", "_")

    if not normalized.startswith(prefix):
        normalized = f"{prefix}{normalized}"

    return normalized


def _get_response_text(content) -> str:
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                return part["text"]
        raise Exception("No text returned by model")

    return str(content)


def _parse_ai_response(raw_response: str) -> dict:
    cleaned_response = raw_response.strip()
    cleaned_response = re.sub(r"^```(?:json)?", "", cleaned_response).strip()
    cleaned_response = re.sub(r"```$", "", cleaned_response).strip()

    match = re.search(r"\{.*\}", cleaned_response, re.DOTALL)
    if match:
        cleaned_response = match.group(0)

    try:
        parsed_response = json.loads(cleaned_response)
    except json.JSONDecodeError:
        parsed_response = ast.literal_eval(cleaned_response)

    if not isinstance(parsed_response, dict):
        raise Exception("AI response is not a valid object")

    return {
        field: str(parsed_response.get(field) or DEFAULT_VALUE)
        for field in RESPONSE_FIELDS
    }


def get_char_made_by_ai(atributtes: dict):
    normalized_attributes = _normalize_attributes(atributtes)
    role_prompt = ROLE_PROMPTS.get(
        normalized_attributes["ai_role"],
        ROLE_PROMPTS["modo_detalhado"],
    )
    prompt_type = PROMPT_TYPES.get(
        normalized_attributes["prompt_type"],
        PROMPT_TYPES["prompt_estruturado"],
    )

    prompt = ChatPromptTemplate.from_template(BASE_PROMPT)
    chain = prompt | _get_llm()
    response = chain.invoke({
        "role_prompt": role_prompt,
        "prompt_type": prompt_type,
        "game": normalized_attributes["game"],
        "name": normalized_attributes["name"],
        "char_class": normalized_attributes["char_class"],
        "race": normalized_attributes["race"],
        "origin": normalized_attributes["origin"],
        "weapon": normalized_attributes["weapon"],
        "god": normalized_attributes["god"],
        "build": normalized_attributes["build"],
    })

    return _parse_ai_response(_get_response_text(response.content))
