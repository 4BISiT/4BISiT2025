# database.py
import sqlite3
import os
import hashlib
import random

DB_NAME = "users.db"

def get_connection():
    """
    Создает и возвращает соединение с базой данных.
    """
    conn = sqlite3.connect(DB_NAME)
    return conn

def hash_answer(answer):
    """
    Возвращает SHA-256 хэш от ответа.
    """
    return hashlib.sha256(answer.encode()).hexdigest()

def initialize_db():
    """
    Инициализирует базу данных, создавая таблицы пользователей и вопросов, а также добавляя суперпользователя.
    """
    if not os.path.exists(DB_NAME):
        conn = get_connection()
        cursor = conn.cursor()
        # Создание таблицы пользователей
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0
            )
        ''')
        # Создание таблицы вопросов
        cursor.execute('''
            CREATE TABLE user_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        # Создаём суперпользователя
        super_username = "admin"
        cursor.execute('''
            INSERT INTO users (username, is_admin)
            VALUES (?, ?)
        ''', (super_username, 1))
        user_id = cursor.lastrowid
        # Добавляем вопросы для суперпользователя
        super_questions = [
            ("Ваш любимый цвет?", "синий"),
            ("Имя вашего первого питомца?", "макс"),
            ("Город вашего рождения?", "москов"),
        ]
        for question, answer in super_questions:
            cursor.execute('''
                INSERT INTO user_questions (user_id, question, answer)
                VALUES (?, ?, ?)
            ''', (user_id, question, hash_answer(answer)))
        conn.commit()
        conn.close()

def get_user_by_username(username):
    """
    Возвращает пользователя по имени.

    :param username: Имя пользователя
    :return: Словарь с данными пользователя или None
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, is_admin FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"id": result[0], "is_admin": bool(result[1])}
    return None

def get_random_question(user_id):
    """
    Возвращает случайный вопрос для пользователя.

    :param user_id: ID пользователя
    :return: Словарь с вопросом и его ID или None
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM user_questions WHERE user_id = ?", (user_id,))
    questions = cursor.fetchall()
    conn.close()
    if questions:
        selected = random.choice(questions)
        return {"question_id": selected[0], "question": selected[1]}
    return None

def verify_answer(question_id, provided_answer):
    """
    Проверяет правильность ответа на вопрос.

    :param question_id: ID вопроса
    :param provided_answer: Предоставленный ответ
    :return: True, если ответ верный, иначе False
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM user_questions WHERE id = ?", (question_id,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == hash_answer(provided_answer):
        return True
    return False

def change_password(user_id, question_id, new_answer):
    """
    Изменяет ответ на конкретный вопрос для пользователя.

    :param user_id: ID пользователя
    :param question_id: ID вопроса
    :param new_answer: Новый ответ
    """
    conn = get_connection()
    cursor = conn.cursor()
    hashed_new_answer = hash_answer(new_answer)
    cursor.execute('''
        UPDATE user_questions
        SET answer = ?
        WHERE id = ? AND user_id = ?
    ''', (hashed_new_answer, question_id, user_id))
    conn.commit()
    conn.close()

def add_user(username, questions_answers, is_admin=0):
    """
    Добавляет нового пользователя с набором вопросов и ответов.

    :param username: Имя пользователя
    :param questions_answers: Список кортежей (question, answer)
    :param is_admin: Флаг администратора
    :return: True если успешно, иначе False
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, is_admin)
            VALUES (?, ?)
        ''', (username, is_admin))
        user_id = cursor.lastrowid
        for question, answer in questions_answers:
            cursor.execute('''
                INSERT INTO user_questions (user_id, question, answer)
                VALUES (?, ?, ?)
            ''', (user_id, question, hash_answer(answer)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_user(username):
    """
    Удаляет пользователя и все его вопросы.

    :param username: Имя пользователя
    :return: True если успешно, иначе False
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0

def modify_user(original_username, new_username=None, new_is_admin=None, new_questions_answers=None):
    """
    Изменяет данные пользователя.

    :param original_username: Текущее имя пользователя
    :param new_username: Новое имя пользователя
    :param new_is_admin: Новый флаг администратора
    :param new_questions_answers: Список кортежей (question_id, new_answer)
    :return: True если успешно, иначе False
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Получаем ID пользователя
        cursor.execute("SELECT id FROM users WHERE username = ?", (original_username,))
        result = cursor.fetchone()
        if not result:
            return False
        user_id = result[0]
        # Обновляем имя пользователя, если необходимо
        if new_username:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
        # Обновляем флаг администратора, если необходимо
        if new_is_admin is not None:
            cursor.execute("UPDATE users SET is_admin = ? WHERE id = ?", (new_is_admin, user_id))
        # Обновляем ответы на вопросы, если необходимо
        if new_questions_answers:
            for question_id, new_answer in new_questions_answers:
                hashed_new_answer = hash_answer(new_answer)
                cursor.execute('''
                    UPDATE user_questions
                    SET answer = ?
                    WHERE id = ? AND user_id = ?
                ''', (hashed_new_answer, question_id, user_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    """
    Возвращает список всех пользователей.

    :return: Список словарей с данными пользователей
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, is_admin FROM users")
    users = cursor.fetchall()
    conn.close()
    return [{"id": user[0], "username": user[1], "is_admin": bool(user[2])} for user in users]

def get_user_questions(user_id):
    """
    Возвращает все вопросы пользователя.

    :param user_id: ID пользователя
    :return: Список словарей с вопросами
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM user_questions WHERE user_id = ?", (user_id,))
    questions = cursor.fetchall()
    conn.close()
    return [{"id": q[0], "question": q[1]} for q in questions]
