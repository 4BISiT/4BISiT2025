# command_processor.py
from PyQt6 import QtWidgets, QtCore
from database import get_user_by_username, get_user_questions
from auth import change_user_answer
from add_user_dialog import AddUserDialog
from delete_user_dialog import DeleteUserDialog
from modify_user_dialog import ModifyUserDialog
from datetime import datetime

class CommandProcessorWindow(QtWidgets.QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.is_admin = self.check_admin()
        self.setWindowTitle("Командный процессор")
        self.setFixedSize(600, 500)
        self.setup_ui()

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс командного процессора.
        """
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Информационная панель
        self.info_label = QtWidgets.QLabel(f"Добро пожаловать, <b>{self.username}</b>!")
        self.info_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-size: 18px;")

        # Поле ввода команды
        self.command_input = QtWidgets.QLineEdit()
        self.command_input.setPlaceholderText("Введите команду")
        self.command_input.setFixedHeight(40)
        self.command_input.returnPressed.connect(self.execute_command)

        # Область вывода
        self.output_area = QtWidgets.QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("font-family: Consolas, 'Courier New', monospace;")

        # Кнопка выхода
        self.logout_button = QtWidgets.QPushButton("Выйти")
        self.logout_button.setFixedHeight(40)
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setStyleSheet("background-color: #e74c3c; border: none; color: white;")
        self.logout_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        # Добавление элементов в макет
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.command_input)
        main_layout.addWidget(self.output_area)
        main_layout.addWidget(self.logout_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self.setLayout(main_layout)

    def check_admin(self):
        """
        Проверяет, является ли текущий пользователь администратором.
        """
        user = get_user_by_username(self.username)
        return user["is_admin"] if user else False

    def execute_command(self):
        """
        Обрабатывает введенную пользователем команду.
        """
        command = self.command_input.text().strip().lower()
        if not command:
            return

        if command == "дата":
            self.display_date()
        elif command == "время":
            self.display_time()
        elif command == "список команд":
            self.display_commands()
        elif self.is_admin and command.startswith("добавление пользователя"):
            self.add_user()
        elif self.is_admin and command.startswith("удаление пользователя"):
            self.delete_user()
        elif self.is_admin and command.startswith("изменение пользователя"):
            self.modify_user()
        elif command.startswith("изменение пароля"):
            self.change_own_password()
        else:
            self.output_area.append("<span style='color: red;'>Неизвестная команда или недостаточно прав.</span>")

        self.command_input.clear()

    def display_date(self):
        """
        Отображает текущую дату.
        """
        current_date = datetime.now().date()
        self.output_area.append(f"<b>Текущая дата:</b> {current_date}")

    def display_time(self):
        """
        Отображает текущее время.
        """
        current_time = datetime.now().time().strftime("%H:%M:%S")
        self.output_area.append(f"<b>Текущее время:</b> {current_time}")

    def display_commands(self):
        """
        Отображает список доступных команд.
        """
        commands = [
            "<b>Дата</b> - отображает текущую дату",
            "<b>Время</b> - отображает текущее время",
            "<b>Список команд</b> - показывает доступные команды",
            "<b>Изменение пароля</b> - изменение своего ответа на вопрос"
        ]
        if self.is_admin:
            admin_commands = [
                "<b>Добавление пользователя</b> - добавляет нового пользователя",
                "<b>Удаление пользователя</b> - удаляет существующего пользователя",
                "<b>Изменение пользователя</b> - изменяет учетную запись пользователя"
            ]
            commands.extend(admin_commands)
        self.output_area.append("<b>Доступные команды:</b>")
        for cmd in commands:
            self.output_area.append(f"• {cmd}")

    def add_user(self):
        """
        Открывает диалог добавления нового пользователя.
        """
        dialog = AddUserDialog()
        if dialog.exec():
            self.output_area.append("<span style='color: green;'>Пользователь успешно добавлен.</span>")

    def delete_user(self):
        """
        Открывает диалог удаления пользователя.
        """
        dialog = DeleteUserDialog(self.username)
        if dialog.exec():
            self.output_area.append("<span style='color: green;'>Пользователь успешно удалён.</span>")

    def modify_user(self):
        """
        Открывает диалог изменения учетной записи пользователя.
        """
        dialog = ModifyUserDialog()
        if dialog.exec():
            self.output_area.append("<span style='color: green;'>Учётная запись пользователя успешно изменена.</span>")

    def change_own_password(self):
        """
        Позволяет пользователю изменить свой ответ на случайно выбранный вопрос.
        """
        dialog = ChangePasswordDialog(self.username)
        if dialog.exec():
            self.output_area.append("<span style='color: green;'>Ваш ответ успешно изменён.</span>")

    def logout(self):
        """
        Выход из системы и возврат к окну входа.
        """
        from login_window import LoginWindow  # Локальный импорт для избежания циклических импортов
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class ChangePasswordDialog(QtWidgets.QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Изменение ответа на вопрос")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс диалога изменения пароля.
        """
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title = QtWidgets.QLabel("Изменение ответа на случайный вопрос")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Поле выбора вопроса
        self.question_combo = QtWidgets.QComboBox()
        self.load_questions()
        self.question_combo.setFixedHeight(40)

        # Поле ввода нового ответа
        self.new_answer_input = QtWidgets.QLineEdit()
        self.new_answer_input.setPlaceholderText("Новый ответ")
        self.new_answer_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.new_answer_input.setFixedHeight(40)

        # Поле подтверждения нового ответа
        self.confirm_answer_input = QtWidgets.QLineEdit()
        self.confirm_answer_input.setPlaceholderText("Подтверждение ответа")
        self.confirm_answer_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_answer_input.setFixedHeight(40)

        # Кнопка сохранения
        self.save_button = QtWidgets.QPushButton("Сохранить")
        self.save_button.setFixedHeight(40)
        self.save_button.clicked.connect(self.save_password)

        # Добавление элементов в макет
        main_layout.addWidget(title)
        main_layout.addWidget(QtWidgets.QLabel("Выберите вопрос:"))
        main_layout.addWidget(self.question_combo)
        main_layout.addWidget(self.new_answer_input)
        main_layout.addWidget(self.confirm_answer_input)
        main_layout.addWidget(self.save_button)

        self.setLayout(main_layout)

    def load_questions(self):
        """
        Загружает вопросы пользователя в комбобокс.
        """
        user = get_user_by_username(self.username)
        if user:
            questions = get_user_questions(user["id"])
            for q in questions:
                self.question_combo.addItem(q["question"], q["id"])

    def save_password(self):
        """
        Сохраняет новый ответ на выбранный вопрос.
        """
        question_id = self.question_combo.currentData()
        new_answer = self.new_answer_input.text().strip()
        confirm_answer = self.confirm_answer_input.text().strip()

        if not new_answer or not confirm_answer:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        if new_answer != confirm_answer:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Ответы не совпадают.")
            return

        change_user_answer(self.username, question_id, new_answer)
        QtWidgets.QMessageBox.information(self, "Успех", "Ваш ответ успешно изменён.")
        self.accept()
