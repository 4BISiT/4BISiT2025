# login_window.py
from PyQt6 import QtWidgets, QtCore
from auth import authenticate, get_user_question
from command_processor import CommandProcessorWindow

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(400, 350)
        self.setup_ui()
        self.current_question = None  # Хранит текущий вопрос и его ID

        # Инициализация таймера для дебаунса
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.load_question)

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс окна входа.
        """
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)

        # Заголовок
        self.title = QtWidgets.QLabel("Добро пожаловать")
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Поле ввода имени пользователя
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setFixedHeight(40)
        # Подключение сигнала textChanged к таймеру
        self.username_input.textChanged.connect(self.on_text_changed)

        # Поле отображения вопроса
        self.question_display = QtWidgets.QLabel("")
        self.question_display.setWordWrap(True)
        self.question_display.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.question_display.setStyleSheet("font-size: 14px;")

        # Поле ввода ответа
        self.answer_input = QtWidgets.QLineEdit()
        self.answer_input.setPlaceholderText("Ответ на вопрос")
        self.answer_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.answer_input.setFixedHeight(40)
        self.answer_input.setEnabled(False)  # Изначально отключено

        # Кнопка входа
        self.login_button = QtWidgets.QPushButton("Войти")
        self.login_button.setFixedHeight(40)
        self.login_button.setEnabled(False)  # Изначально отключено
        self.login_button.clicked.connect(self.handle_login)

        # Кнопка сброса
        self.reset_button = QtWidgets.QPushButton("Сбросить")
        self.reset_button.setFixedHeight(40)
        self.reset_button.clicked.connect(self.reset_fields)

        # Добавление элементов в макет
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.username_input)
        self.main_layout.addWidget(self.question_display)
        self.main_layout.addWidget(self.answer_input)
        self.main_layout.addWidget(self.login_button)
        self.main_layout.addWidget(self.reset_button)

        self.setLayout(self.main_layout)

    def on_text_changed(self, text):
        """
        Обработчик изменения текста в поле ввода имени пользователя.
        Запускает таймер для дебаунса.
        """
        # Сброс таймера при каждом изменении текста
        self.timer.start(500)  # Задержка 500 мс

    def load_question(self):
        """
        Загружает случайный вопрос для введенного имени пользователя.
        """
        username = self.username_input.text().strip()
        if username:
            question_data = get_user_question(username)
            if question_data:
                self.current_question = question_data
                self.question_display.setText(f"Вопрос: {question_data['question']}")
                self.answer_input.setEnabled(True)
                self.login_button.setEnabled(True)
            else:
                self.question_display.setText("Пользователь не найден или отсутствуют вопросы.")
                self.answer_input.setEnabled(False)
                self.login_button.setEnabled(False)
        else:
            self.question_display.setText("")
            self.answer_input.setEnabled(False)
            self.login_button.setEnabled(False)

    def handle_login(self):
        """
        Обрабатывает попытку входа пользователя.
        """
        username = self.username_input.text().strip()
        answer = self.answer_input.text().strip()
        if not username or not answer:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите имя пользователя и ответ.")
            return
        if not self.current_question:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Вопрос не загружен.")
            return
        if authenticate(username, self.current_question["question_id"], answer):
            # Открываем главное окно и передаём имя пользователя
            self.main_window = CommandProcessorWindow(username)
            self.main_window.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный ответ на вопрос.")
            self.answer_input.clear()

    def reset_fields(self):
        """
        Сбрасывает поля ввода.
        """
        self.username_input.clear()
        self.question_display.setText("")
        self.answer_input.clear()
        self.answer_input.setEnabled(False)
        self.login_button.setEnabled(False)
        self.current_question = None
        self.timer.stop()  # Останавливаем таймер при сбросе
