from typing import NamedTuple, Optional
from handler.Advertisement import Advertisement


class Message(NamedTuple):
    amount: Optional[int]
    output_text: str

class Last_at():
    last_at: str

# проверяем правильность url и коректируем
def get_update_avito_url(tg_message: str) -> Message:
    # if message ...avito then false else true
    if _false_parse_message(tg_message):
        false_message = "Неправильно введена ссылка"
        return Message(amount=1, output_text=false_message)
    tg_message += '&p=1'
    return Message(amount=None, output_text=tg_message)


# парсим страницу и создаем сообщение для пользователя
def get_url(tg_message: str):
    output_message = ''
    ad = Advertisement(tg_message)
    list_ad_avito = ad.get_urls(last_url=Last_at.last_at)
    if list_ad_avito is None:
        return output_message

    Last_at.last_at = list_ad_avito[0].href

    for i in list_ad_avito:
        output_message += 'Обявление: ' + i.name + \
                          '\nЦена: ' + str(i.price) + \
                            '\nОписание: ' + i.description +\
                          '\nСсылка: ' + i.href + '\n'

    return output_message


def update_last_url(tg_message: str) -> str:
    ad = Advertisement(tg_message)
    Last_at.last_at = ad.get_last_url()
    return Last_at.last_at


def _false_parse_message(_message: str) -> bool:
    if _message[:20] != "https://www.avito.ru":
        return True
    else:
        return False

