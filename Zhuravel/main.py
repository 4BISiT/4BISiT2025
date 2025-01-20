# main.py
import sys
from PyQt6 import QtWidgets, QtCore
from database import initialize_db
from login_window import LoginWindow

def main():
    """
    Основная функция для запуска приложения.
    """
    # Инициализация базы данных
    initialize_db()

    # Создание приложения
    app = QtWidgets.QApplication(sys.argv)

    # Загрузка стилей из файла styles.qss
    try:
        with open("styles.qss", "r", encoding="utf-8") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Файл стилей styles.qss не найден.")

    # Создание и отображение окна входа
    login = LoginWindow()
    login.show()

    # Запуск цикла приложения
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
