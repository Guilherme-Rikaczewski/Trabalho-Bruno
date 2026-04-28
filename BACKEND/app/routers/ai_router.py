from fastapi import APIRouter, HTTPException
from app.schemas.ai_schema import AiResponse, CharacterAtributtes
import app.services.ai_service as ai
import ast


router = APIRouter(prefix="/ai", tags=["AI"])
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post('/create/', response_model=AiResponse)
def generete_character(atributtes: CharacterAtributtes):
    try:
        char_atributtes = {
            'game': atributtes.game,
            'name': atributtes.name,
            'race': atributtes.race,
            'char_class': atributtes.char_class,
            'origin': atributtes.origin,
            'weapon': atributtes.weapon,
            'god': atributtes.god,
            'build': atributtes.build,
        }

        ai_generated_char = ai.get_char_made_by_ai(char_atributtes)
        ai_generated_char_dict = ast.literal_eval(ai_generated_char)
        return ai_generated_char_dict
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(500, detail=f'Internal server error {error}')
