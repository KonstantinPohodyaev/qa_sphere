from pydantic import BaseModel


class LogoutResponse(BaseModel):
    '''Ответ на запрос выхода из системы'''

    message: str = 'Успешный выход из системы'
