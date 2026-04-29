# TRABALHO BRUNO

try:
    from google import genai
    import app.services.ai_service as ai


    print("Criando personagem com IA")
    print("Preencha os campos a seguir, caso não queira preencher algum")
    print("apenas deixe em branco, a IA escolhe para você")


    game: str | None = str(input("Nome do jogo (Exemplo: d&d): "))
    name: str | None = str(input("Nome do personagem (Exemplo: Bruno): "))
    race: str | None = str(input("Raça do personagem (Exemplo: Elfo): "))
    char_class: str | None = str(input("Classe do personagem (Exemplo: Mago ou Guerreiro): "))
    origin: str | None = str(input("Origem do personagem (Exemplo: Mercenario): "))
    weapon: str | None = str(input("Arma usada do personagem (Exemplo: Machado ou Espada): "))
    god: str | None = str(input("Deus seguido pelo personagem (Exemplo: Selune da Luz): "))
    build: str | None = str(input("Build do personagem (Exemplo: Mago de fogo): "))

    if game == '':
        game = None

    if name == '':
        name = None

    if race == '':
        race = None

    if char_class == '':
        char_class = None

    if origin == '':
        origin = None

    if weapon == '':
        weapon = None

    if god == '':
        god = None

    if build == '':
        build = None

    char = ai.get_char_made_by_ai({
        'game': game,
        'name': name,
        'race': race,
        'char_class': char_class,
        'origin': origin,
        'weapon': weapon,
        'god': god,
        'build': build,
    })

    print()
    print()
    print(char)
except ModuleNotFoundError:
    print('Você pode estar rodando o código sem ter instalado as dependencias')
    print('Lembre de criar um VENV para rodar o codigo: python -m venv venv')
    print('Também ative o ambiente virtual com venv\\Scripts\\activate')
    print('Rode pip install -r requirements.txt')
    print('Você deve estar na pasta \\BACKEND pelo CMD para executar os comandos')
    print('Se você estiver rodando usando o botão do VSCode')
    print('isso pode apresentar problemas de dependencias')
    print('Prefira executar pelo comando: python validacao_api.py')
    print('diretamente pelo CMD')
    print('Você deve estar na pasta \\BACKEND pelo CMD para executar o comando')
except genai.errors.ServerError as error:
    print(error)
    print('RESUMINDO: OS SERVIDORES DA GOOGLE ESTÃO SOBRECARREGADOS, TENTE NOVAMENTE MAIS TARDE')
except ValueError as error:
    print(error)
    print('SUA CHAVE DE API NÃO ESTÁ NO .env')
    print('VOCÊ PRECISA RENOMEAR O ARQUIVO .env-example PARA .env')
    print('ENTÃO COLOQUE A --> SUA <-- CHAVE DE API DA GOOGLE GEMINI NA VARIAVEL GEMINI_API_KEY=')  
