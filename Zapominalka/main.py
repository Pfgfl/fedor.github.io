import sys
import os
import re
import random
import sqlite3
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QWidget,
    QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QHBoxLayout, QGroupBox, QRadioButton, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class UserPreferences:
    """
    Класс для управления пользовательскими предпочтениями и сохранения данных авторизации
    """
    def __init__(self):
        # Файл для хранения пользовательских данных
        self.prefs_file = "user_preferences.json"

    def save_user_credentials(self, login, password):
        # Сохраняет логин и пароль в JSON файл
        prefs = {
            "login": login,
            "password": password
        }
        with open(self.prefs_file, 'w', encoding='utf-8') as f:
            json.dump(prefs, f)

    def load_user_credentials(self):
        # Загружает сохраненные учетные данные из файла
        if os.path.exists(self.prefs_file):
            with open(self.prefs_file, 'r', encoding='utf-8') as f:
                prefs = json.load(f)
                return prefs.get("login"), prefs.get("password")
        return None, None

    def clear_credentials(self):
        # Удаляет файл с учетными данными при выходе
        if os.path.exists(self.prefs_file):
            os.remove(self.prefs_file)


class Database:
    """
    Класс для работы с базой данных SQLite
    """
    def __init__(self):
        self.db_name = "zapominalka.db"
        self.init_database()

    def init_database(self):
        # Инициализация базы данных и создание таблиц
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Удаление старых таблиц (для очистки при разработке)
        cursor.execute('DROP TABLE IF EXISTS user_unknown_words')
        cursor.execute('DROP TABLE IF EXISTS user_known_words')
        cursor.execute('DROP TABLE IF EXISTS remembered_user')
        cursor.execute('DROP TABLE IF EXISTS words')

        # Создание таблицы пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                level TEXT NOT NULL DEFAULT 'Начинающий (A1)'
            )
        ''')

        # Создание таблицы для неизученных слов пользователя
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_unknown_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                translation TEXT NOT NULL,
                level TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, word, level)
            )
        ''')

        conn.commit()
        conn.close()

    def user_exists(self, login):
        # Проверяет, существует ли пользователь с таким логином
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
        result = cursor.fetchone() is not None
        conn.close()
        return result

    def create_user(self, login, password):
        # Создает нового пользователя в базе данных
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)",
                       (login, password))
        conn.commit()
        conn.close()

    def verify_user(self, login, password):
        # Проверяет правильность логина и пароля
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE login = ? AND password = ?",
                       (login, password))
        result = cursor.fetchone() is not None
        conn.close()
        return result

    def get_user_level(self, login):
        # Получает уровень пользователя из базы данных
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT level FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "Начинающий (A1)"

    def set_user_level(self, login, level):
        # Обновляет уровень пользователя
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET level = ? WHERE login = ?", (level, login))
        conn.commit()
        conn.close()

    def get_user_id(self, login):
        # Получает ID пользователя по логину
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def add_unknown_word(self, user_id, word, translation, level):
        # Добавляет слово в список неизученных для пользователя
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO user_unknown_words (user_id, word, translation, level) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, word, translation, level))
        conn.commit()
        conn.close()

    def remove_unknown_word(self, user_id, word, level):
        # Удаляет слово из списка неизученных (когда пользователь его выучил)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM user_unknown_words 
            WHERE user_id = ? AND word = ? AND level = ?
        ''', (user_id, word, level))
        conn.commit()
        conn.close()

    def get_unknown_words(self, user_id):
        # Получает все неизученные слова пользователя
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT word, translation, level 
            FROM user_unknown_words 
            WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchall()
        conn.close()
        return result

    def is_word_unknown(self, user_id, word, level):
        # Проверяет, находится ли слово в списке неизученных
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM user_unknown_words 
            WHERE user_id = ? AND word = ? AND level = ?
        ''', (user_id, word, level))
        result = cursor.fetchone() is not None
        conn.close()
        return result


class LoginWindow(QMainWindow):
    """
    Окно входа и регистрации пользователя
    """
    def __init__(self):
        super().__init__()
        self.db = Database()  # Объект для работы с базой данных
        self.prefs = UserPreferences()  # Объект для работы с настройками
        self.initUI()  # Инициализация интерфейса

    def initUI(self):
        # Настройка основного окна
        self.setWindowTitle('Вход / Регистрация')
        self.setFixedSize(400, 300)

        # Создание центрального виджета и основного layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Заголовок окна
        title_label = QLabel('Войдите или зарегистрируйтесь')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        layout.addWidget(title_label)

        layout.addSpacing(20)

        # Поле для ввода логина
        self.login_field = QLineEdit()
        self.login_field.setPlaceholderText('Логин')
        self.login_field.setStyleSheet("padding: 8px; border: 1px solid #ccc;")
        layout.addWidget(self.login_field)

        # Поле для ввода пароля
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText('Пароль')
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setStyleSheet("padding: 8px; border: 1px solid #ccc;")
        layout.addWidget(self.password_field)

        # Поле для повторения пароля (показывается только при регистрации)
        self.repeat_password_field = QLineEdit()
        self.repeat_password_field.setPlaceholderText('Повторите пароль')
        self.repeat_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.repeat_password_field.hide()
        self.repeat_password_field.setStyleSheet("padding: 8px; border: 1px solid #ccc;")
        layout.addWidget(self.repeat_password_field)

        layout.addSpacing(10)

        # Кнопка входа
        self.login_button = QPushButton('Войти')
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.login_button)

        # Кнопка перехода к регистрации
        self.register_button = QPushButton('Создать аккаунт')
        self.register_button.clicked.connect(self.show_register_fields)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.register_button)

    def show_register_fields(self):
        # Показывает дополнительные поля для регистрации
        self.repeat_password_field.show()
        self.register_button.hide()
        self.login_button.setText("Создать аккаунт")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.register_user)

    def handle_login(self):
        # Обрабатывает попытку входа
        login = self.login_field.text().strip()
        password = self.password_field.text().strip()

        if self.db.verify_user(login, password):
            # Если пользователь существует, сохраняем учетные данные и открываем главное меню
            self.prefs.save_user_credentials(login, password)
            user_level = self.db.get_user_level(login)
            self.open_main_window(login, user_level)
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильный логин или пароль.")

    def register_user(self):
        # Обрабатывает регистрацию нового пользователя
        login = self.login_field.text().strip()
        password = self.password_field.text().strip()
        repeat = self.repeat_password_field.text().strip()

        # Валидация логина (только буквы, цифры, дефис и подчеркивание)
        if not re.match(r"^[A-Za-z0-9_-]+$", login):
            QMessageBox.warning(self, "Ошибка", "Логин может содержать только буквы, цифры, '-' и '_'.")
            return

        # Проверка совпадения паролей
        if password != repeat:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return

        # Проверка существования пользователя
        if self.db.user_exists(login):
            QMessageBox.warning(self, "Ошибка", "Такой логин уже существует.")
            return

        # Создание пользователя и сохранение учетных данных
        self.db.create_user(login, password)
        self.prefs.save_user_credentials(login, password)

        QMessageBox.information(self, "Готово", "Регистрация успешна!")
        self.open_main_window(login, "Начинающий (A1)")

    def open_main_window(self, username, user_level):
        # Открывает главное меню и скрывает окно входа
        self.hide()
        self.main_menu = MainMenu(username, user_level, self.db, self.prefs)
        self.main_menu.show()


class MainMenu(QWidget):
    """
    Главное меню приложения после успешного входа
    """
    def __init__(self, username, user_level, db, prefs):
        super().__init__()
        self.username = username
        self.user_level = user_level
        self.db = db
        self.prefs = prefs
        self.user_id = db.get_user_id(username)  # Получаем ID пользователя
        self.initUI()

    def initUI(self):
        # Настройка главного меню
        self.setWindowTitle(f'Главное меню - {self.username}')
        self.setFixedSize(500, 450)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Приветственная надпись
        welcome_label = QLabel(f'Добро пожаловать, {self.username}!')
        welcome_label.setWordWrap(True)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        layout.addWidget(welcome_label)

        layout.addSpacing(20)

        # Группа для выбора уровня изучения
        level_group = QGroupBox("Выберите уровень для изучения:")
        level_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        level_layout = QVBoxLayout()

        # Радиокнопки для выбора уровня
        self.radio_beginner = QRadioButton("Начинающий (A1)")
        self.radio_intermediate = QRadioButton("Средний (B1)")
        self.radio_advanced = QRadioButton("Продвинутый (C1)")

        level_layout.addWidget(self.radio_beginner)
        level_layout.addWidget(self.radio_intermediate)
        level_layout.addWidget(self.radio_advanced)
        level_group.setLayout(level_layout)

        layout.addWidget(level_group)

        # Устанавливаем текущий уровень пользователя
        if self.user_level == "Начинающий (A1)":
            self.radio_beginner.setChecked(True)
        elif self.user_level == "Средний (B1)":
            self.radio_intermediate.setChecked(True)
        elif self.user_level == "Продвинутый (C1)":
            self.radio_advanced.setChecked(True)
        else:
            self.radio_beginner.setChecked(True)

        # Подключаем обработчики изменения уровня
        self.radio_beginner.toggled.connect(self.on_level_changed)
        self.radio_intermediate.toggled.connect(self.on_level_changed)
        self.radio_advanced.toggled.connect(self.on_level_changed)

        layout.addSpacing(20)

        # Кнопка для изучения новых слов
        self.learn_button = QPushButton('Учить новые слова')
        self.learn_button.clicked.connect(self.open_learning_window)
        self.learn_button.setFont(QFont('Arial', 12))
        self.learn_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.learn_button)

        # Кнопка для повторения слов
        self.review_button = QPushButton('Повторять слова')
        self.review_button.clicked.connect(self.open_review_window)
        self.review_button.setFont(QFont('Arial', 12))
        self.review_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.review_button)

        layout.addSpacing(10)

        # Кнопка выхода из аккаунта
        self.logout_button = QPushButton('Выйти из аккаунта')
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.logout_button)

    def get_selected_level(self):
        # Возвращает выбранный уровень изучения
        if self.radio_beginner.isChecked():
            return "Начинающий (A1)"
        elif self.radio_intermediate.isChecked():
            return "Средний (B1)"
        elif self.radio_advanced.isChecked():
            return "Продвинутый (C1)"
        else:
            return "Начинающий (A1)"

    def on_level_changed(self):
        # Обрабатывает изменение уровня изучения
        if not any([self.radio_beginner.isChecked(),
                    self.radio_intermediate.isChecked(),
                    self.radio_advanced.isChecked()]):
            return

        selected_level = self.get_selected_level()
        self.db.set_user_level(self.username, selected_level)  # Сохраняем уровень в БД
        self.user_level = selected_level

    def open_learning_window(self):
        # Открывает окно изучения новых слов
        selected_level = self.get_selected_level()
        self.learning_window = LearningWindow(self.username, selected_level, self.db, self.prefs)
        self.learning_window.show()
        self.close()

    def open_review_window(self):
        # Открывает окно повторения слов
        unknown_words = self.db.get_unknown_words(self.user_id)
        if not unknown_words:
            QMessageBox.warning(self, "Нет слов для повторения", "У вас пока нет слов для повторения!")
            return

        self.review_window = ReviewWindow(self.username, self.db, self.prefs)
        self.review_window.show()
        self.close()

    def logout(self):
        # Выход из аккаунта
        self.prefs.clear_credentials()  # Удаляем сохраненные учетные данные
        self.login_window = LoginWindow()  # Возвращаемся к окну входа
        self.login_window.show()
        self.close()


class LearningWindow(QWidget):
    """
    Окно для изучения новых слов
    """
    def __init__(self, username, level, db, prefs):
        super().__init__()
        self.username = username
        self.level = level
        self.db = db
        self.prefs = prefs
        self.user_id = db.get_user_id(username)
        self.current_mode = "en_to_ru"  # Режим перевода по умолчанию
        self.current_word = None  # Текущее слово для изучения
        self.words = []  # Список слов для изучения

        self.load_words()  # Загрузка слов из файла
        self.initUI()  # Инициализация интерфейса
        self.start_learning()  # Начало процесса обучения

    def initUI(self):
        # Настройка окна изучения слов
        self.setWindowTitle(f'Учить слова - {self.username} ({self.level})')
        self.setFixedSize(500, 450)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Панель выбора режима перевода
        mode_layout = QHBoxLayout()
        mode_label = QLabel('Режим перевода:')
        mode_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Английский → Русский", "en_to_ru")
        self.mode_combo.addItem("Русский → Английский", "ru_to_en")
        self.mode_combo.currentTextChanged.connect(self.change_mode)
        self.mode_combo.setStyleSheet("padding: 5px;")

        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)

        layout.addSpacing(20)

        # Метка для отображения вопроса
        self.question_label = QLabel('', self)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.question_label.setStyleSheet("background-color: #f0f0f0; padding: 20px; border-radius: 5px;")
        self.question_label.setMinimumHeight(80)
        layout.addWidget(self.question_label)

        layout.addSpacing(10)

        # Поле для ввода ответа
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText('Введите перевод...')
        self.answer_input.returnPressed.connect(self.check_answer)  # Enter для проверки
        self.answer_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc;")
        layout.addWidget(self.answer_input)

        # Кнопка проверки ответа
        self.check_button = QPushButton('Проверить')
        self.check_button.clicked.connect(self.check_answer)
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.check_button)

        # Метка для отображения результата
        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont('Arial', 12))
        self.result_label.setMinimumHeight(40)
        layout.addWidget(self.result_label)

        # Кнопка показа правильного ответа
        self.show_answer_button = QPushButton('Показать ответ')
        self.show_answer_button.clicked.connect(self.show_answer)
        self.show_answer_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.show_answer_button)

        # Кнопка перехода к следующему слову
        self.next_button = QPushButton('Следующее слово')
        self.next_button.clicked.connect(self.next_word)
        self.next_button.setEnabled(False)  # Изначально неактивна
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        layout.addWidget(self.next_button)

        layout.addSpacing(10)

        # Кнопка возврата в главное меню
        self.back_button = QPushButton('Вернуться в главное меню')
        self.back_button.clicked.connect(self.return_to_main_menu)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.back_button)

    def load_words(self):
        # Загрузка слов из файлов в зависимости от уровня
        level_files = {
            "Начинающий (A1)": "beginner.txt",
            "Средний (B1)": "intermediate.txt",
            "Продвинутый (C1)": "advanced.txt"
        }

        filename = level_files.get(self.level, "beginner.txt")

        # Чтение слов из файла
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            all_words = [line.strip().split(',') for line in lines if line.strip()]

        # Фильтрация слов: оставляем только те, которые пользователь еще не изучал
        self.words = [word for word in all_words
                      if not self.db.is_word_unknown(self.user_id, word[0], self.level)]
        random.shuffle(self.words)  # Перемешиваем слова для случайного порядка

        if not self.words:
            # Если все слова изучены, показываем сообщение
            QMessageBox.information(self, 'Информация', 'Вы изучили все новые слова для этого уровня!')
            self.return_to_main_menu()
            return

    def change_mode(self):
        # Смена режима перевода (английский-русский или русский-английский)
        self.current_mode = self.mode_combo.currentData()
        if self.current_word:
            self.display_current_word()  # Обновляем отображение текущего слова

    def display_current_word(self):
        # Отображает текущее слово в зависимости от выбранного режима
        if self.current_mode == "en_to_ru":
            self.question_label.setText(f'Переведите на русский: {self.current_word[0]}')
        else:
            self.question_label.setText(f'Переведите на английский: {self.current_word[1]}')

        # Сбрасываем состояние интерфейса
        self.answer_input.clear()
        self.result_label.clear()
        self.answer_input.setEnabled(True)
        self.check_button.setEnabled(True)
        self.show_answer_button.setEnabled(True)
        self.next_button.setEnabled(False)

    def start_learning(self):
        # Начинает процесс обучения
        self.next_word()

    def next_word(self):
        # Переход к следующему слову
        if not self.words:
            # Если слова закончились, показываем сообщение
            QMessageBox.information(self, 'Информация', 'Вы изучили все новые слова для этого уровня!')
            self.return_to_main_menu()
            return

        self.current_word = self.words.pop()  # Берем следующее слово из списка
        self.display_current_word()

    def check_answer(self):
        # Проверка введенного пользователем ответа
        user_answer = self.answer_input.text().strip().lower()

        # Определяем правильный ответ в зависимости от режима
        if self.current_mode == "en_to_ru":
            correct_answer = self.current_word[1].lower()
        else:
            correct_answer = self.current_word[0].lower()

        if user_answer == correct_answer:
            # Правильный ответ
            self.result_label.setText('✓ Правильно!')
            self.result_label.setStyleSheet('color: green; font-weight: bold;')
        else:
            # Неправильный ответ - добавляем слово в список неизученных
            self.result_label.setText(f'✗ Неправильно. Правильный ответ: {correct_answer}')
            self.result_label.setStyleSheet('color: red; font-weight: bold;')
            self.db.add_unknown_word(self.user_id, self.current_word[0], self.current_word[1], self.level)

        # Обновляем состояние интерфейса после проверки
        self.answer_input.setEnabled(False)
        self.check_button.setEnabled(False)
        self.show_answer_button.setEnabled(False)
        self.next_button.setEnabled(True)

    def show_answer(self):
        # Показывает правильный ответ без проверки
        if self.current_mode == "en_to_ru":
            correct_answer = self.current_word[1]
        else:
            correct_answer = self.current_word[0]

        self.result_label.setText(f'Правильный ответ: {correct_answer}')
        self.result_label.setStyleSheet('color: blue; font-weight: bold;')

        # Добавляем слово в список неизученных (т.к. пользователь не смог ответить)
        self.db.add_unknown_word(self.user_id, self.current_word[0], self.current_word[1], self.level)

        # Обновляем состояние интерфейса
        self.answer_input.setEnabled(False)
        self.check_button.setEnabled(False)
        self.show_answer_button.setEnabled(False)
        self.next_button.setEnabled(True)

    def return_to_main_menu(self):
        # Возврат в главное меню
        user_level = self.db.get_user_level(self.username)
        self.main_menu = MainMenu(self.username, user_level, self.db, self.prefs)
        self.main_menu.show()
        self.close()


class ReviewWindow(QWidget):
    """
    Окно для повторения ранее изученных слов
    """
    def __init__(self, username, db, prefs):
        super().__init__()
        self.username = username
        self.db = db
        self.prefs = prefs
        self.user_id = db.get_user_id(username)
        self.current_mode = "en_to_ru"
        self.current_word = None
        self.words = []

        self.load_words()  # Загрузка слов для повторения
        self.initUI()  # Инициализация интерфейса
        self.start_review()  # Начало процесса повторения

    def initUI(self):
        # Настройка окна повторения (аналогично окну изучения)
        self.setWindowTitle(f'Повторять слова - {self.username}')
        self.setFixedSize(500, 450)

        layout = QVBoxLayout()
        self.setLayout(layout)

        mode_layout = QHBoxLayout()
        mode_label = QLabel('Режим перевода:')
        mode_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Английский → Русский", "en_to_ru")
        self.mode_combo.addItem("Русский → Английский", "ru_to_en")
        self.mode_combo.currentTextChanged.connect(self.change_mode)
        self.mode_combo.setStyleSheet("padding: 5px;")

        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)

        layout.addSpacing(20)

        self.question_label = QLabel('', self)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.question_label.setStyleSheet("background-color: #f0f0f0; padding: 20px; border-radius: 5px;")
        self.question_label.setMinimumHeight(80)
        layout.addWidget(self.question_label)

        layout.addSpacing(10)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText('Введите перевод...')
        self.answer_input.returnPressed.connect(self.check_answer)
        self.answer_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc;")
        layout.addWidget(self.answer_input)

        self.check_button = QPushButton('Проверить')
        self.check_button.clicked.connect(self.check_answer)
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.check_button)

        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont('Arial', 12))
        self.result_label.setMinimumHeight(40)
        layout.addWidget(self.result_label)

        self.show_answer_button = QPushButton('Показать ответ')
        self.show_answer_button.clicked.connect(self.show_answer)
        self.show_answer_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.show_answer_button)

        self.next_button = QPushButton('Следующее слово')
        self.next_button.clicked.connect(self.next_word)
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        layout.addWidget(self.next_button)

        layout.addSpacing(10)

        self.back_button = QPushButton('Вернуться в главное меню')
        self.back_button.clicked.connect(self.return_to_main_menu)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        layout.addWidget(self.back_button)

    def load_words(self):
        # Загрузка слов для повторения из базы данных
        self.words = self.db.get_unknown_words(self.user_id)
        random.shuffle(self.words)  # Перемешиваем слова

        if not self.words:
            QMessageBox.information(self, 'Информация', 'Нет слов для повторения!')
            self.return_to_main_menu()
            return

    def change_mode(self):
        # Смена режима перевода
        self.current_mode = self.mode_combo.currentData()
        if self.current_word:
            self.display_current_word()

    def display_current_word(self):
        # Отображение текущего слова
        if self.current_mode == "en_to_ru":
            self.question_label.setText(f'Переведите на русский: {self.current_word[0]}')
        else:
            self.question_label.setText(f'Переведите на английский: {self.current_word[1]}')

        self.answer_input.clear()
        self.result_label.clear()
        self.answer_input.setEnabled(True)
        self.check_button.setEnabled(True)
        self.show_answer_button.setEnabled(True)
        self.next_button.setEnabled(False)

    def start_review(self):
        # Начало процесса повторения
        self.next_word()

    def next_word(self):
        # Переход к следующему слову
        if not self.words:
            QMessageBox.information(self, 'Информация', 'Вы повторили все слова!')
            self.return_to_main_menu()
            return

        self.current_word = self.words.pop()
        self.display_current_word()

    def check_answer(self):
        # Проверка ответа пользователя
        user_answer = self.answer_input.text().strip().lower()

        if self.current_mode == "en_to_ru":
            correct_answer = self.current_word[1].lower()
        else:
            correct_answer = self.current_word[0].lower()

        if user_answer == correct_answer:
            # Правильный ответ - удаляем слово из списка неизученных
            self.result_label.setText('✓ Правильно!')
            self.result_label.setStyleSheet('color: green; font-weight: bold;')
            self.db.remove_unknown_word(self.user_id, self.current_word[0], self.current_word[2])
        else:
            # Неправильный ответ - оставляем слово в списке
            self.result_label.setText(f'✗ Неправильно. Правильный ответ: {correct_answer}')
            self.result_label.setStyleSheet('color: red; font-weight: bold;')

        self.answer_input.setEnabled(False)
        self.check_button.setEnabled(False)
        self.show_answer_button.setEnabled(False)
        self.next_button.setEnabled(True)

    def show_answer(self):
        # Показ правильного ответа
        if self.current_mode == "en_to_ru":
            correct_answer = self.current_word[1]
        else:
            correct_answer = self.current_word[0]

        self.result_label.setText(f'Правильный ответ: {correct_answer}')
        self.result_label.setStyleSheet('color: blue; font-weight: bold;')

        self.answer_input.setEnabled(False)
        self.check_button.setEnabled(False)
        self.show_answer_button.setEnabled(False)
        self.next_button.setEnabled(True)

    def return_to_main_menu(self):
        # Возврат в главное меню
        user_level = self.db.get_user_level(self.username)
        self.main_menu = MainMenu(self.username, user_level, self.db, self.prefs)
        self.main_menu.show()
        self.close()


if __name__ == '__main__':
    # Создание и запуск приложения
    app = QApplication(sys.argv)

    prefs = UserPreferences()
    login, password = prefs.load_user_credentials()  # Пытаемся загрузить сохраненные учетные данные

    if login and password:
        # Если есть сохраненные данные, проверяем их
        db = Database()
        if db.verify_user(login, password):
            # Автоматический вход
            user_level = db.get_user_level(login)
            main_menu = MainMenu(login, user_level, db, prefs)
            main_menu.show()
        else:
            # Если данные неверные, очищаем и показываем окно входа
            prefs.clear_credentials()
            login_window = LoginWindow()
            login_window.show()
    else:
        # Если нет сохраненных данных, показываем окно входа
        login_window = LoginWindow()
        login_window.show()

    sys.exit(app.exec())