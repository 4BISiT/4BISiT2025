# add_user_dialog.py
from PyQt6 import QtWidgets, QtCore
from database import add_user
import sqlite3

class AddUserDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление пользователя")
        self.setFixedSize(500, 600)
        self.setup_ui()

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс диалога добавления пользователя.
        """
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Заголовок
        title = QtWidgets.QLabel("Добавление нового пользователя")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Поля ввода
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setFixedHeight(40)

        # Секция вопросов
        self.questions_layout = QtWidgets.QVBoxLayout()
        self.questions_layout.setSpacing(10)

        self.add_question_button = QtWidgets.QPushButton("Добавить вопрос")
        self.add_question_button.setFixedHeight(40)
        self.add_question_button.clicked.connect(self.add_question_field)

        # Добавление первого вопроса по умолчанию
        self.add_question_field()

        # Кнопка добавления
        self.add_button = QtWidgets.QPushButton("Добавить пользователя")
        self.add_button.setFixedHeight(40)
        self.add_button.clicked.connect(self.add_user)

        # Добавление элементов в макет
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(self.username_input)
        self.main_layout.addWidget(QtWidgets.QLabel("Вопросы для аутентификации:"))
        self.main_layout.addLayout(self.questions_layout)
        self.main_layout.addWidget(self.add_question_button)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.add_button)

        self.setLayout(self.main_layout)

    def add_question_field(self):
        """
        Добавляет набор полей для ввода вопроса и ответа.
        """
        question_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(10)

        question_input = QtWidgets.QLineEdit()
        question_input.setPlaceholderText("Вопрос")
        question_input.setFixedHeight(40)

        answer_input = QtWidgets.QLineEdit()
        answer_input.setPlaceholderText("Ответ")
        answer_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        answer_input.setFixedHeight(40)

        remove_button = QtWidgets.QPushButton("Удалить")
        remove_button.setFixedHeight(40)
        remove_button.setStyleSheet("background-color: #e74c3c; color: white;")
        remove_button.clicked.connect(lambda: self.remove_question_field(question_widget))

        layout.addWidget(question_input)
        layout.addWidget(answer_input)
        layout.addWidget(remove_button)
        question_widget.setLayout(layout)

        self.questions_layout.addWidget(question_widget)

    def remove_question_field(self, widget):
        """
        Удаляет набор полей для вопроса и ответа.

        :param widget: Виджет, который нужно удалить
        """
        self.questions_layout.removeWidget(widget)
        widget.deleteLater()

    def add_user(self):
        """
        Добавляет нового пользователя в базу данных.
        """
        username = self.username_input.text().strip()
        if not username:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите имя пользователя.")
            return

        questions_answers = []
        for i in range(self.questions_layout.count()):
            widget = self.questions_layout.itemAt(i).widget()
            if widget:
                q_input = widget.findChild(QtWidgets.QLineEdit, "")
                a_input = widget.findChildren(QtWidgets.QLineEdit, "")[1]
                question = q_input.text().strip()
                answer = a_input.text().strip()
                if question and answer:
                    questions_answers.append((question, answer))
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все вопросы и ответы.")
                    return

        if not questions_answers:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один вопрос и ответ.")
            return

        # Получение статуса администратора
        is_admin = QtWidgets.QMessageBox.question(
            self, "Администратор", "Является ли пользователь администратором?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        is_admin_flag = 1 if is_admin == QtWidgets.QMessageBox.StandardButton.Yes else 0

        success = add_user(username, questions_answers, is_admin_flag)
        if success:
            QtWidgets.QMessageBox.information(self, "Успех", "Пользователь добавлен.")
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Имя пользователя уже существует или произошла ошибка.")
