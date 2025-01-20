# modify_user_dialog.py
from PyQt6 import QtWidgets, QtCore
from database import get_all_users, get_user_questions, modify_user, get_user_by_username
import sqlite3

class ModifyUserDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменение учетной записи пользователя")
        self.setFixedSize(500, 600)
        self.setup_ui()

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс диалога изменения учетной записи пользователя.
        """
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Заголовок
        title = QtWidgets.QLabel("Изменение учетной записи пользователя")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Поле выбора пользователя
        self.user_combo = QtWidgets.QComboBox()
        self.load_users()
        self.user_combo.currentTextChanged.connect(self.load_user_details)
        self.user_combo.setFixedHeight(40)

        # Поля для изменения данных
        self.new_username_input = QtWidgets.QLineEdit()
        self.new_username_input.setPlaceholderText("Новое имя пользователя")
        self.new_username_input.setFixedHeight(40)

        self.is_admin_checkbox = QtWidgets.QCheckBox("Администратор")

        # Секция вопросов
        self.questions_layout = QtWidgets.QVBoxLayout()
        self.questions_layout.setSpacing(10)

        self.add_question_button = QtWidgets.QPushButton("Добавить новый вопрос")
        self.add_question_button.setFixedHeight(40)
        self.add_question_button.clicked.connect(self.add_question_field)

        # Кнопка сохранения изменений
        self.save_button = QtWidgets.QPushButton("Сохранить изменения")
        self.save_button.setFixedHeight(40)
        self.save_button.clicked.connect(self.modify_user)

        # Добавление элементов в макет
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(QtWidgets.QLabel("Выберите пользователя:"))
        self.main_layout.addWidget(self.user_combo)
        self.main_layout.addWidget(QtWidgets.QLabel("Новое имя пользователя:"))
        self.main_layout.addWidget(self.new_username_input)
        self.main_layout.addWidget(self.is_admin_checkbox)
        self.main_layout.addWidget(QtWidgets.QLabel("Изменение ответов на вопросы:"))
        self.main_layout.addLayout(self.questions_layout)
        self.main_layout.addWidget(self.add_question_button)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.save_button)

        self.setLayout(self.main_layout)

    def load_users(self):
        """
        Загружает список пользователей в комбобокс.
        """
        users = get_all_users()
        for user in users:
            self.user_combo.addItem(user["username"])

    def load_user_details(self, username):
        """
        Загружает текущие данные выбранного пользователя.
        """
        if not username:
            return
        user = get_user_by_username(username)
        if user:
            self.new_username_input.setText(username)
            self.is_admin_checkbox.setChecked(user["is_admin"])
            # Очистка предыдущих вопросов
            while self.questions_layout.count():
                item = self.questions_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            # Загрузка вопросов пользователя
            questions = get_user_questions(user["id"])
            for q in questions:
                self.add_existing_question_field(q["id"], q["question"])

    def add_existing_question_field(self, question_id, question_text):
        """
        Добавляет набор полей для существующего вопроса и его ответа.

        :param question_id: ID вопроса
        :param question_text: Текст вопроса
        """
        question_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(10)

        question_label = QtWidgets.QLabel(question_text)
        question_label.setFixedWidth(150)

        answer_input = QtWidgets.QLineEdit()
        answer_input.setPlaceholderText("Новый ответ")
        answer_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        answer_input.setFixedHeight(40)

        save_button = QtWidgets.QPushButton("Сохранить")
        save_button.setFixedHeight(40)
        save_button.clicked.connect(lambda: self.save_answer(question_id, answer_input))

        layout.addWidget(question_label)
        layout.addWidget(answer_input)
        layout.addWidget(save_button)
        question_widget.setLayout(layout)

        self.questions_layout.addWidget(question_widget)

    def add_question_field(self):
        """
        Добавляет набор полей для ввода нового вопроса и ответа.
        """
        question_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(10)

        question_input = QtWidgets.QLineEdit()
        question_input.setPlaceholderText("Новый вопрос")
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
        Удаляет набор полей для нового вопроса и ответа.

        :param widget: Виджет, который нужно удалить
        """
        self.questions_layout.removeWidget(widget)
        widget.deleteLater()

    def save_answer(self, question_id, answer_input):
        """
        Сохраняет новый ответ на существующий вопрос.

        :param question_id: ID вопроса
        :param answer_input: Поле ввода нового ответа
        """
        new_answer = answer_input.text().strip()
        if not new_answer:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите новый ответ.")
            return
        change_user_answer(self.user_combo.currentText(), question_id, new_answer)
        QtWidgets.QMessageBox.information(self, "Успех", "Ответ успешно изменён.")
        answer_input.clear()

    def modify_user(self):
        """
        Применяет изменения к учетной записи пользователя.
        """
        original_username = self.user_combo.currentText()
        new_username = self.new_username_input.text().strip()
        is_admin = 1 if self.is_admin_checkbox.isChecked() else 0

        if not new_username:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите новое имя пользователя.")
            return

        success = modify_user(original_username, new_username=new_username, new_is_admin=is_admin)
        if success:
            QtWidgets.QMessageBox.information(self, "Успех", "Учётная запись пользователя изменена.")
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Произошла ошибка при изменении учётной записи.")
