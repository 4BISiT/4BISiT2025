# delete_user_dialog.py
from PyQt6 import QtWidgets, QtCore
from database import get_all_users, delete_user

class DeleteUserDialog(QtWidgets.QDialog):
    def __init__(self, current_username):
        super().__init__()
        self.current_username = current_username
        self.setWindowTitle("Удаление пользователя")
        self.setFixedSize(400, 400)
        self.setup_ui()

    def setup_ui(self):
        """
        Настраивает пользовательский интерфейс диалога удаления пользователя.
        """
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title = QtWidgets.QLabel("Удаление пользователя")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Список пользователей
        self.user_list = QtWidgets.QListWidget()
        self.load_users()
        self.user_list.setFixedHeight(200)

        # Кнопка удаления
        self.delete_button = QtWidgets.QPushButton("Удалить выбранного пользователя")
        self.delete_button.setFixedHeight(40)
        self.delete_button.clicked.connect(self.delete_user)

        # Добавление элементов в макет
        main_layout.addWidget(title)
        main_layout.addWidget(QtWidgets.QLabel("Выберите пользователя для удаления:"))
        main_layout.addWidget(self.user_list)
        main_layout.addWidget(self.delete_button)

        self.setLayout(main_layout)

    def load_users(self):
        """
        Загружает список пользователей в список выбора.
        """
        users = get_all_users()
        for user in users:
            username = user["username"]
            if username != self.current_username:
                self.user_list.addItem(username)

    def delete_user(self):
        """
        Удаляет выбранного пользователя из базы данных.
        """
        selected_items = self.user_list.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите пользователя для удаления.")
            return
        username_to_delete = selected_items[0].text()
        confirmation = QtWidgets.QMessageBox.question(
            self, "Подтверждение", f"Вы уверены, что хотите удалить пользователя '{username_to_delete}'?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirmation == QtWidgets.QMessageBox.StandardButton.Yes:
            success = delete_user(username_to_delete)
            if success:
                QtWidgets.QMessageBox.information(self, "Успех", f"Пользователь '{username_to_delete}' удалён.")
                self.accept()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Произошла ошибка при удалении пользователя.")
