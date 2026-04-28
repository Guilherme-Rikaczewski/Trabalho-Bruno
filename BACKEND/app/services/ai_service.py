from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()


def get_char_made_by_ai(atributtes: dict):
    for k, v in atributtes.items():
        if v is None:
            atributtes[f'{k}'] = 'Not specified'
    print(atributtes)
    client = genai.Client()
    first_part = f"""Create the lore and some characteristics for a medieval
    RPG character based on the following attributes.
    If an characteristic is not specified, chose a random one.

    Game System: {atributtes['game']};
    Character Name: {atributtes['name']};
    Class: {atributtes['char_class']};
    Race: {atributtes['race']};
    Origin: {atributtes['origin']};
    Favorite Weapon: {atributtes['weapon']};
    Serves the fictional god from the chosen system: {atributtes['god']};
    Planned build: {atributtes['build']};

    """
    seconde_part = """Please answer only EXACTLY in this format:
    {
        'game': 'your_text',
        'name': 'your_text',
        'char_class': 'your_text',
        'race': 'your_text',
        'origin': 'your_text',
        'weapon': 'your_text',
        'god': 'your_text',
        'build': 'your_text',
        'lore': 'your_text',
        'physical_characteristics': 'your_text',
        'personality_traits': 'your_text',
        'other_characteristics': 'your_text',
    }

    The answer must be like a python dict
    where each key have just a simple text.
    """

    prompt = first_part + seconde_part

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="low")
        )
    )

    return response.text


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
