from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from google.genai import types
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


def get_char_made_by_ai(atributtes: dict):
    for k in atributtes:
        if atributtes[k] is None:
            atributtes[k] = "Not specified"

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=api_key,
        temperature=0.7
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are a Dungeon Master for a D&D game.

        Answer ONLY with a valid Python dict.
        Do not use markdown.
        Do not explain anything.
        Do not wrap with ```.

        Format:

        {{
            'game': 'text',
            'name': 'text',
            'char_class': 'text',
            'race': 'text',
            'origin': 'text',
            'weapon': 'text',
            'god': 'text',
            'build': 'text',
            'lore': 'text',
            'physical_characteristics': 'text',
            'personality_traits': 'text',
            'other_characteristics': 'text'
        }}

        Request:
        {pergunta}
        """
    )

    chain = prompt | llm

    pergunta_usuario = f"""
    Create the lore and characteristics for a medieval RPG character.

    Game System: {atributtes['game']}
    Character Name: {atributtes['name']}
    Class: {atributtes['char_class']}
    Race: {atributtes['race']}
    Origin: {atributtes['origin']}
    Favorite Weapon: {atributtes['weapon']}
    God: {atributtes['god']}
    Build: {atributtes['build']}
    """

    resposta = chain.invoke({
        "pergunta": pergunta_usuario
    })

    content = resposta.content

    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                return part["text"]

        raise Exception("No text returned by model")

    return str(content)


# char = get_char_made_by_ai({
#     'game': 'd&d',
#     'name': None,
#     'race': None,
#     'char_class': 'mage',
#     'origin': None,
#     'weapon': None,
#     'god': None,
#     'build': 'fire mage',
# })
# print()
# print()
# print(char)
