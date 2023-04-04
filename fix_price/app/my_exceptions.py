from requests import Response
from typing import Optional


class ResponseErrorCode(Exception):
    """Веб-запрос вернул код ошибки"""

    def __init__(self, response: Response, message: Optional[str] = None):
        self.response = response

        if message is None:
            self.message = f"Веб-запрос вернул код ошибки {response.status_code}\n" \
                           f"Запрашиваемый ресурс: {response.url}\n" \
                           f"Ответ сервера:\n" \
                           f"{response.json()}"
        else:
            self.message = message

        super().__init__(self.message)
