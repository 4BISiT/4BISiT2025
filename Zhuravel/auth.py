# auth.py
from database import get_user_by_username, get_random_question, verify_answer, change_password

def authenticate(username, question_id, provided_answer):
    """
    Проверяет подлинность пользователя по имени и ответу на вопрос.

    :param username: Имя пользователя
    :param question_id: ID вопроса
    :param provided_answer: Ответ пользователя
    :return: True, если аутентификация успешна, иначе False
    """
    user = get_user_by_username(username)
    if not user:
        return False
    return verify_answer(question_id, provided_answer)

def get_user_question(username):
    """
    Возвращает случайный вопрос для аутентификации пользователя.

    :param username: Имя пользователя
    :return: Словарь с вопросом и его ID или None, если пользователь не найден
    """
    user = get_user_by_username(username)
    if not user:
        return None
    return get_random_question(user["id"])

def change_user_answer(username, question_id, new_answer):
    """
    Изменяет ответ на конкретный вопрос для пользователя.

    :param username: Имя пользователя
    :param question_id: ID вопроса
    :param new_answer: Новый ответ
    """
    user = get_user_by_username(username)
    if user:
        change_password(user["id"], question_id, new_answer)
