from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random
import pickle
import sys
import pygame
from pygame import mixer
from pygame.mixer import music


class NoticeWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    # Инициализация окна с кратким объявлением
    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        #  Работа с файлом для построчного считывания и объединения строк, добавление получившегося текста в виджет
        self.file = open(r"etc/Notice.txt", "r", encoding="utf-8")
        self.rules_text = ' '.join(str(x) for x in self.file.readlines())
        self.file.close()
        self.label_text = QLabel(self.rules_text)
        self.label_text.setFont(QFont("Comic Sans MS", 12))
        self.label_text.setWordWrap(True)
        self.layout.addWidget(self.label_text, 0, 0)
        # Создание кнопки "Ок" для открытия главного меню, присоединение конпки к виджету
        self.btn_ok = QPushButton("Ок", self)
        self.btn_ok.setStyleSheet("background: rgb(0,190,255);")
        self.btn_ok.setFont(QFont("Comic Sans MS", 12))
        self.btn_ok.setFixedSize(100, 35)
        self.btn_ok.clicked.connect(self.gotoMainWindow)
        self.layout.addWidget(self.btn_ok, 1, 0)
        # Оформление окна, добавление иконки, фона
        self.setWindowTitle("Предупреждение")
        self.setWindowIcon(QIcon(r"pictures/quad_icon.jpg"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(QPixmap(r"pictures/snowflakes.png")))
        self.setPalette(self.palette)
        self.show()

    # Переход в главное меню
    def gotoMainWindow(self):
        sound_click.play()
        self.close()
        self.main_menu = MainMenu()


class MainMenu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    # Инициализация главного меню
    def initUI(self):
        # Создание кнопки "Играть" для запуска окна по добавлению никнейма игрока (метод goto_add_nickname)
        self.btn_play = QPushButton("Играть", self)
        self.btn_play.setFont(QFont("Comic Sans MS", 12))
        self.btn_play.setToolTip("Эта кнопка вызывает <b>NicknameMenu</b> виджет")
        self.btn_play.setStyleSheet("background: rgb(0,191,255);")
        self.btn_play.resize(260, 35)
        self.btn_play.move(0, 0)
        self.btn_play.clicked.connect(self.gotoAddNickname)
        # Создание кнопки "Таблица рекордов" для запуска окна с соответствующим списком игроков (метод goto_leaderboard)
        self.btn_leaderboard = QPushButton("Таблица рекордов", self)
        self.btn_leaderboard.setFont(QFont("Comic Sans MS", 12))
        self.btn_leaderboard.setToolTip("Эта кнопка вызывает <b>LeaderboardWindow</b> виджет")
        self.btn_leaderboard.setStyleSheet("background: rgb(0,144,255);")
        self.btn_leaderboard.resize(260, 35)
        self.btn_leaderboard.move(0, 35)
        self.btn_leaderboard.clicked.connect(self.gotoLeaderboard)
        # Создание кнопки "Правила" для запуска окна с управлением, правилами и описанием игры (метод goto_rules)
        self.btn_rules = QPushButton("Правила", self)
        self.btn_rules.setFont(QFont("Comic Sans MS", 12))
        self.btn_rules.setToolTip("Эта кнопка вызывает <b>RulesWindow</b> виджет")
        self.btn_rules.setStyleSheet("background: rgb(100,149,237);")
        self.btn_rules.resize(260, 35)
        self.btn_rules.move(0, 70)
        self.btn_rules.clicked.connect(self.gotoRules)
        # Создание кнопки "Выход" для запуска окна для выхода из игры (метод goto_exit)
        self.btn_exit = QPushButton("Выход", self)
        self.btn_exit.setFont(QFont("Comic Sans MS", 12))
        self.btn_exit.setToolTip("Эта кнопка вызывает <b>ExitWindow</b> виджет")
        self.btn_exit.setStyleSheet("background: rgb(123,104,238);")
        self.btn_exit.resize(260, 35)
        self.btn_exit.move(0, 105)
        self.btn_exit.clicked.connect(self.gotoExit)
        # Оформление окна, добавление иконки, шрифтов
        self.setFixedSize(260, 140)
        self.setWindowTitle("Меню")
        self.setWindowIcon(QIcon(r"pictures/quad_icon.jpg"))
        QToolTip.setFont(QFont("Comic Sans MS", 12))
        self.show()

    # Переход в окно по добавлению никнейма
    def gotoAddNickname(self):
        sound_click.play()
        self.nickname_user = NicknameMenu()

    # Переход в окно c рекордами
    def gotoLeaderboard(self):
        sound_click.play()
        self.leaderboard = LeaderboardWindow()

    # Переход в окно с правилами
    def gotoRules(self):
        sound_click.play()
        self.rules = RulesWindow()

    # Переход в окно с выходом из игры
    def gotoExit(self):
        sound_click.play()
        self.exit_window = ExitWindow()


class NicknameMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.textboxValue = ""
        self.initUI()

    # Инициализация окна для ввода никнейма и последующего начала игры
    def initUI(self):
        # Создание области с подсказкой для ввода никнейма
        self.text_box = QLineEdit(self)
        self.text_box.setPlaceholderText("Введите свой ник (3 буквы):")
        self.text_box.resize(220, 30)
        self.text_box.move(20, 20)
        # Создание кнопки "Ввод" для считывания по нажатию никнейма игрока
        self.btn_inpup = QPushButton("Ввод", self)
        self.btn_inpup.setStyleSheet("background: rgb(0,190,255);")
        self.btn_inpup.setFont(QFont("Comic Sans MS", 12))
        self.btn_inpup.setFixedSize(100, 35)
        self.btn_inpup.move(20, 80)
        self.btn_inpup.clicked.connect(self.onClick)
        # Оформление окна, добавление иконки, фона
        self.setFixedSize(260, 140)
        self.setWindowTitle("Ник")
        self.setWindowIcon(QIcon(r"pictures/quad_icon.jpg"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(QPixmap(r"pictures/snowflakes.png")))
        self.setPalette(self.palette)
        self.show()

    # Считывание нажатие кнопки и запуск игры с введёным никнеймом
    def onClick(self):
        sound_click.play()
        self.textboxValue = self.text_box.text()
        if self.textboxValue == "":
            self.textboxValue = "nOn"
        self.quadrapassel_game = Quadrapassel(self.textboxValue)
        self.close()


class LeaderboardWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    # Инициализация окна с таблицей рекордов (топ-5)
    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # Создание сетки в виджете, добавление к сетке текста, получаемого методом get_leaders()
        self.label = QLabel(self.getLeaders())
        self.label.setFont(QFont("Comic Sans MS", 12))
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label, 0, 0)
        # Создание кнопки "Назад" для возвращения в главное меню, присоединение к сетке виджета
        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setStyleSheet("background: rgb(0,190,255);")
        self.btn_back.setFont(QFont("Comic Sans MS", 12))
        self.btn_back.setFixedSize(100, 35)
        self.btn_back.clicked.connect(self.closeWindow)
        self.layout.addWidget(self.btn_back, 1, 0)
        # Оформление окна, добавление иконки, фона
        self.setFixedSize(260, 260)
        self.setWindowTitle("Топ-5")
        self.setWindowIcon(QIcon(r"pictures/quad_icon.jpg"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(QPixmap(r"pictures/snowflakes.png")))
        self.setPalette(self.palette)
        self.show()

    # Считывание из файла таблицы результатов игроков, сортировка и возвращение из функции топ-5 игроков в виде строки
    def getLeaders(self):
        with open(r"etc/leaderboard", "rb") as f:
            leaders = pickle.load(f)
            if leaders:
                leaders.sort(key=lambda x: x["score"], reverse=True)
        result = "Лидеры\n"
        count = 0
        for i in leaders[:5]:
            count += 1
            result += str(count) + ". " + str(i["name"])[:3] + " - " + str(i["score"]) + "\n"
        return result

    # Закрытие окна
    def closeWindow(self):
        sound_click.play()
        self.close()


class RulesWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    # Инициализация окна с описанием правил игры и управлением
    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        #  Работа с файлом для построчного считывания и объединения строк, добавление получившегося текста в виджет
        self.file = open(r"etc/Rules.txt", "r", encoding="utf-8")
        self.rules_text = ' '.join(str(x) for x in self.file.readlines())
        self.file.close()
        self.label_text = QLabel(self.rules_text)
        self.label_text.setFont(QFont("Comic Sans MS", 12))
        self.label_text.setWordWrap(True)
        self.layout.addWidget(self.label_text, 0, 0)
        # Создание кнопки "Назад" для возвращения в главное меню, присоединение конпки к виджету
        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setStyleSheet("background: rgb(0,190,255);")
        self.btn_back.setFont(QFont("Comic Sans MS", 12))
        self.btn_back.setFixedSize(100, 35)
        self.btn_back.clicked.connect(self.closeWindow)
        self.layout.addWidget(self.btn_back, 1, 0)
        # Оформление окна, добавление иконки, фона
        self.setWindowTitle("Правила")
        self.setWindowIcon(QIcon(r"pictures/quad_icon.jpg"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(QPixmap(r"pictures/snowflakes.png")))
        self.setPalette(self.palette)
        self.show()

    # Закрытие окна
    def closeWindow(self):
        sound_click.play()
        self.close()


class ExitWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    # Инициализация окна выхода из программы
    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # Создание текста с вопросом, присоединение к сетке виджета
        self.question_text = QLabel("Вы уверены?")
        self.question_text.setAlignment(Qt.AlignCenter)
        self.question_text.setFont(QFont("Comic Sans MS", 12))
        self.layout.addWidget(self.question_text, 0, 0, 1, 2)
        # Создание кнопки "Да" для выхода из приложения, присоединение к сетке виджета
        self.btn_yes = QPushButton("Да", self)
        self.btn_yes.setStyleSheet("background: rgb(255,0,100);")
        self.btn_yes.setFont(QFont("Comic Sans MS", 12))
        self.btn_yes.setFixedSize(100, 35)
        self.btn_yes.clicked.connect(self.closeApp)
        self.layout.addWidget(self.btn_yes, 1, 0)
        # Создание кнопки "Нет" для возвращения в главное меню, присоединение к сетке виджета
        self.btn_no = QPushButton("Нет", self)
        self.btn_no.setStyleSheet("background: rgb(0,190,255);")
        self.btn_no.setFont(QFont("Comic Sans MS", 12))
        self.btn_no.setFixedSize(100, 35)
        self.btn_no.clicked.connect(self.closeWindow)
        self.layout.addWidget(self.btn_no, 1, 1)
        # Оформление окна, добавление иконки, фона
        self.setFixedSize(260, 140)
        self.setWindowTitle("Выход")
        self.setWindowIcon(QIcon(r"pictures/quad_icon.jpg"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(QPixmap(r"pictures/snowflakes.png")))
        self.setPalette(self.palette)
        self.show()

    # Закрытие приложения
    def closeApp(self):
        sound_click.play()
        QCoreApplication.instance().quit()

    # Закрытие окна
    def closeWindow(self):
        sound_click.play()
        self.close()


class Quadrapassel(QWidget):

    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.initUI()

    # Инициализация окна с игрой
    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        # Добавление игрового поля
        self.quad_board = GameBoard(self, self.user_name)
        self.quad_board.setFixedSize(356, 560)
        self.quad_board.setStyleSheet("border-style: solid; border-width: 3px; border-color: black;")
        self.layout.addWidget(self.quad_board, 0, 0, 4, 4)
        # Добавление окна со следующей фигурой
        self.next_piece_board = QLabel(self)
        self.next_piece_pic = QPixmap(r"pictures/shape_0.png")
        self.next_piece_board.setPixmap(self.next_piece_pic)
        self.next_piece_board.setFixedSize(106, 106)
        self.next_piece_board.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.next_piece_board, 0, 5)
        # Добавление qr-ссылки на github
        self.qr_info = QLabel(self)
        self.qr_code = QPixmap(r"pictures/qr.png")
        self.qr_info.setPixmap(self.qr_code)
        self.qr_info.setFixedSize(200, 200)
        self.qr_info.setAlignment(Qt.AlignCenter)
        self.qr_info.setStyleSheet("border-style: solid; border-width: 3px; border-color: black; border-radius: 8px")
        self.layout.addWidget(self.qr_info, 1, 5)
        # Добавление окно с прогрессом игры
        self.hot_key = QLabel(self)
        self.hot_key.setText("Выход <-> CTRL + Q\nРестарт <-> ALT + R\nПауза <-> P")
        self.hot_key.setFixedSize(200, 100)
        self.hot_key.setFont(QFont("Comic Sans MS", 10))
        self.hot_key.setStyleSheet("border-style: solid; border-width: 3px; border-color: black; border-radius: 8px")
        self.layout.addWidget(self.hot_key, 2, 5)
        # Добавление окно с выводом очков и уровня сложности
        self.info_label = QLabel(self)
        self.info_label.setFixedSize(200, 70)
        self.info_label.setFont(QFont("Comic Sans MS", 10))
        self.info_label.setStyleSheet("border-style: solid; border-width: 3px; border-color: black; border-radius: 8px")
        self.layout.addWidget(self.info_label, 3, 5)
        # Добавление иконки, названия, фона и запуск игры
        self.setFixedSize(600, 600)
        self.setWindowTitle("Quadrapassel 2.0")
        self.setWindowIcon(QIcon(r"pictures/quad_icon.jpg"))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(QPixmap(r"pictures/snowflakes.png")))
        self.setPalette(self.palette)
        self.quad_board.startGame()
        self.show()


class GameBoard(QFrame):

    def __init__(self, parent, user):
        super().__init__(parent)
        self.passel = parent
        self.user = user
        self.initUI()

    # Инициализация игрового поля
    def initUI(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.game_timer = QBasicTimer()
        self.cur_piece = Shape()
        self.next_piece = Shape()
        self.refresh_rate = 400
        self.board_weigth = 14
        self.board_height = 22
        self.square_side = 25
        self.cur_pos_x = 0
        self.cur_pos_y = 0
        self.score = 0
        self.level = 1
        self.is_bonus = False
        self.is_playing = False
        self.is_paused = False
        self.is_active = True
        self.game_board = [TypeShape.empty_shape for _ in range(self.board_height * self.board_weigth)]

    # Запуск игрового таймера и создание первой фигуры
    def startGame(self):
        self.is_playing = True
        self.startFirstPiece()
        self.passel.info_label.setText("Level: " + str(self.level) + "\nScore: " + str(self.score))
        self.game_timer.start(self.refresh_rate, self)

    # Создание первой фигуры отдельной итерацией, т.к. активную фигуру нужно считать из следующей, которой пока что нет
    def startFirstPiece(self):
        self.next_piece.setRandomShape(self.level)
        self.newPiece()

    # Обычный цикл создания фигуры
    def newPiece(self):
        self.cur_piece.setShape(self.next_piece.num_shape)
        self.cur_pos_x = self.board_weigth // 2
        self.cur_pos_y = self.board_height - 1 + self.cur_piece.startPos()
        self.checkGameOver()
        self.setNextPiece()

    # Установка картинки-подсказки следующей фигуры
    def setNextPiece(self):
        self.next_piece.setRandomShape(self.level)
        self.passel.next_piece_pic = QPixmap(r"pictures/shape_" + str(self.next_piece.num_shape) + ".png")
        self.passel.next_piece_board.setPixmap(self.passel.next_piece_pic)

    # Проверка возможности создания фигуры, в случае проигрыша запись результатов в отдельных файл
    def checkGameOver(self):
        if not self.tryMove(self.cur_piece, self.cur_pos_x, self.cur_pos_y):
            sound_game_over.play()
            self.cur_piece.setShape(TypeShape.empty_shape)
            self.game_timer.stop()
            self.is_playing = False
            self.passel.info_label.setText("GAME OVER")
            with open(r"etc/leaderboard", "rb") as f:
                leaders = pickle.load(f)
                leaders += [{"name": self.user, "score": self.score}]
            with open(r"etc/leaderboard", "wb") as f:
                pickle.dump(leaders, f)

    # Считывание клавиатуры
    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()
        # Фикс бага, когда активная фигура при удаления линии могла "провалиться"
        if not self.is_playing or self.cur_piece.num_shape == TypeShape.empty_shape:
            super(GameBoard, self).keyPressEvent(event)
            return
        # Реализация преждевременного выхода из игры
        if mod == Qt.ControlModifier:
            if key == Qt.Key_Q:
                self.passel.close()
        # Реализация рестарта игры
        elif mod == Qt.AltModifier:
            if key == Qt.Key_R:
                self.new_game = Quadrapassel(self.passel.user_name)
                self.passel.close()
        # Реализация паузы в игре
        if key == Qt.Key_P:
            self.pauseGame()
            return
        # Запрет дальнейшей обработки движений, если игра на паузе
        if self.is_paused:
            return
        # Движение фигуры влево
        elif key == Qt.Key_Left:
            self.tryMove(self.cur_piece, self.cur_pos_x - 1, self.cur_pos_y)
        # Движение фигуры вправо
        elif key == Qt.Key_Right:
            self.tryMove(self.cur_piece, self.cur_pos_x + 1, self.cur_pos_y)
        # Поворот фигуры
        elif key == Qt.Key_Up:
            self.tryMove(self.cur_piece.rotateShape(), self.cur_pos_x, self.cur_pos_y)
        # Проброс фигуры в самый низ
        elif key == Qt.Key_Space:
            self.spaceDown()
        # Движение фигуры вниз на 1 клетку
        elif key == Qt.Key_Down:
            self.oneLineDown()
        # Дальнейшая обработка нажатий
        else:
            super(GameBoard, self).keyPressEvent(event)

    # Функция остановки игры
    def pauseGame(self):
        if self.is_paused:
            self.game_timer.start(self.refresh_rate, self)
            self.passel.info_label.setText("Level: " + str(self.level) + "\nScore: " + str(self.score))
            self.is_paused = False
        else:
            self.game_timer.stop()
            self.passel.info_label.setText("PAUSED")
            self.is_paused = True
        self.update()

    # Мгновенный проброс фигуры вниз
    def spaceDown(self):
        new_y = self.cur_pos_y
        while new_y > 0:
            if not self.tryMove(self.cur_piece, self.cur_pos_x, new_y - 1):
                break
            new_y -= 1
        self.checkShapeActive()

    # Падение фигуры на 1 клетку вниз, вызываемое либо игроком, либо таймером
    def oneLineDown(self):
        if not self.tryMove(self.cur_piece, self.cur_pos_x, self.cur_pos_y - 1):
            self.checkShapeActive()

    # Проверка активности фигуры
    def checkShapeActive(self):
        for i in range(4):
            x = self.cur_pos_x + self.cur_piece.getX(i)
            y = self.cur_pos_y - self.cur_piece.getY(i)
            self.setShape(x, y, self.cur_piece.num_shape)
        self.checkFullLines()
        if self.is_active:
            self.newPiece()
            if random.randint(1, 10) > 7:
                if self.is_bonus:
                    self.addBonusLine()
                    self.is_bonus = False

    def timerEvent(self, event):
        if event.timerId() == self.game_timer.timerId():
            if self.is_active:
                self.oneLineDown()
            else:
                self.is_active = True
                self.newPiece()
        else:
            super(GameBoard, self).timerEvent(event)

    # Определение координат для отрисовки игрового поля по секциям/квадратам
    def paintEvent(self, event):
        painter = QPainter(self)
        game_board = self.contentsRect()
        board_top = game_board.bottom() - self.board_height * self.square_side + 1
        for i in range(self.board_height):
            for j in range(self.board_weigth):
                square = self.getShape(j, self.board_height - i - 1)
                if square != TypeShape.empty_shape:
                    self.drawSquare(painter, game_board.left() + j * self.square_side,
                                    board_top + i * self.square_side, square)
        if self.cur_piece.num_shape != TypeShape.empty_shape:
            for i in range(4):
                x = self.cur_pos_x + self.cur_piece.getX(i)
                y = self.cur_pos_y - self.cur_piece.getY(i)
                self.drawSquare(painter, game_board.left() + x * self.square_side,
                                board_top + (self.board_height - y - 1) * self.square_side,
                                self.cur_piece.num_shape)

    # Отрисовка отдельных квадратов игрового поля
    def drawSquare(self, painter, x, y, shape):
        colorTable = [(0x000000, 0x000000), (0x8a2be2, 0x320b35),
                      (0x217ca3, 0xe29030), (0x00ffff, 0x739f3d),
                      (0x803e75, 0x00fa9a), (0xe73f0b, 0xa11f0c),
                      (0xb8d20b, 0xf77604), (0x283655, 0xd0f1e9),
                      (0xb6ff01, 0x000000)]
        color1 = QColor(colorTable[shape][0])
        color2 = QColor(colorTable[shape][1])
        for i in range(self.square_side // 2 - 1):
            painter.fillRect(x + 1 + i, y + 1 + i, self.square_side - (i + 1) * 2,
                             self.square_side - (i + 1) * 2, color1 if i % 2 else color2)
        painter.setPen(QColor.lighter(color1))
        painter.drawLine(x, y + self.square_side - 1, x, y)
        painter.drawLine(x, y, x + self.square_side - 1, y)
        painter.setPen(QColor.darker(color1))
        painter.drawLine(x + 1, y + self.square_side - 1, x + self.square_side - 1, y + self.square_side - 1)
        painter.drawLine(x + self.square_side - 1, y + self.square_side - 1, x + self.square_side - 1, y + 1)

    # Проверка наличия заполненных линий и их удаление
    def checkFullLines(self):
        num_full_lines = 0
        list_full_line = []
        for i in range(self.board_height):
            n = 0
            for j in range(self.board_weigth):
                if not self.getShape(j, i) == TypeShape.empty_shape:
                    n = n + 1
            if n == self.board_weigth:
                list_full_line.append(i)
        list_full_line.reverse()
        for i in list_full_line:
            for j in range(i, self.board_height - 1):
                for k in range(self.board_weigth):
                    self.setShape(k, j, self.getShape(k, j + 1))
        num_full_lines = num_full_lines + len(list_full_line)
        if num_full_lines > 0:
            self.addPoint(num_full_lines)
            self.is_active = False
            self.cur_piece.setShape(TypeShape.empty_shape)
            self.update()

    # Увеличение уровня и начисление очков
    def addPoint(self, point):
        self.score += point * 10 * self.level
        if self.score >= 50 and self.level == 1:
            self.refresh_rate = 400
            self.level = 2
            self.game_timer.start(self.refresh_rate, self)
        if self.score >= 150 and self.level == 2:
            self.refresh_rate = 300
            self.level = 3
            self.game_timer.start(self.refresh_rate, self)
        if self.score >= 300 and self.level == 3:
            self.refresh_rate = 250
            self.level = 4
            self.game_timer.start(self.refresh_rate, self)
        if self.score >= 400 and self.level >= 4:
            self.level = 5
            if random.randint(1, 10) > 5:
                self.is_bonus = True
        self.passel.info_label.setText("Level: " + str(self.level) + "\nScore: " + str(self.score))

    # Проверка возможности занятия нового места активной фигурой
    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.getX(i)
            y = newY - newPiece.getY(i)
            if x < 0 or x >= self.board_weigth or y < 0 or y >= self.board_height:
                return False
            if self.getShape(x, y) != TypeShape.empty_shape:
                return False
        self.cur_piece = newPiece
        self.cur_pos_x = newX
        self.cur_pos_y = newY
        self.update()
        return True

    # Добавление "бонусной" линии - полной линии с 1 пропуском
    def addBonusLine(self):
        num_empty_square = random.randint(0, 13)
        for y in range(self.board_height - 2, -1, -1):
            for x in range(self.board_weigth):
                self.setShape(x, y, self.getShape(x, y - 1))
        for x in range(self.board_weigth):
            if x != num_empty_square:
                self.setShape(x, 0, random.randint(1, 8))

    # Получение фигуры в данном квадрате игрового поля
    def getShape(self, x, y):
        return self.game_board[(y * self.board_weigth) + x]

    # Установка фигуры в данном квадрате игрового поля
    def setShape(self, x, y, shape):
        self.game_board[(y * self.board_weigth) + x] = shape


class TypeShape(object):
    # Номера фигур
    empty_shape = 0
    line_shape = 1
    reverse_s_shape = 2
    s_shape = 3
    t_shape = 4
    square_shape = 5
    l_shape = 6
    reverse_l_shape = 7
    troll_shape = 8
    # Таблица координат точек отрисовки фигур
    shape_coords_table = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((-1, 0), (0, 0), (1, 0), (0, -1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (-1, 0), (-1, 1), (0, 1)),
        ((0, 1), (1, 1), (1, 0), (1, -1)),
        ((0, 0), (-1, -1), (0, -2), (1, -1))
    )


class Shape(object):

    def __init__(self):
        self.coords = [[0, 0] for _ in range(4)]
        self.num_shape = TypeShape.empty_shape
        self.setShape(TypeShape.empty_shape)

    # Заполнение таблицы координат по номеру фигуры
    def setShape(self, shape):
        table = TypeShape.shape_coords_table[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]
        self.num_shape = shape

    # Создание случайной фигуры в зависимости от уровня игры
    def setRandomShape(self, level):
        if level < 3:
            self.setShape(random.randint(1, 7))
        elif level == 3:
            if random.randint(1, 8) == 8:
                if random.randint(1, 10) > 7:
                    self.setShape(8)
            else:
                self.setShape(random.randint(1, 7))
        elif level >= 4:
            if random.randint(2, 8) == 8:
                if random.randint(1, 10) > 7:
                    self.setShape(8)
            else:
                self.setShape(random.randint(2, 7))

    # Получение х-координаты
    def getX(self, index):
        return self.coords[index][0]

    # Получение у-координат
    def getY(self, index):
        return self.coords[index][1]

    # Назначение х-координаты
    def setX(self, index, x):
        self.coords[index][0] = x

    # Назначение у-координаты
    def setY(self, index, y):
        self.coords[index][1] = y

    # Нахождение координаты нижней точки фигуры
    def startPos(self):
        min_y = self.coords[0][1]
        for i in range(4):
            min_y = min(min_y, self.coords[i][1])
        return min_y

    # Поворот фигуры
    def rotateShape(self):
        if self.num_shape in [5, 8]:
            return self
        result = Shape()
        result.num_shape = self.num_shape
        for i in range(4):
            result.setX(i, self.getY(i))
            result.setY(i, -self.getX(i))
        return result


if __name__ == '__main__':
    app = QApplication([])
    pygame.init()
    pygame.mixer.init()
    sound_click = mixer.Sound(r"music/click.wav")
    sound_game_over = mixer.Sound(r"music/gg.wav")
    music.load("music/theme.wav")
    music.play(-1)
    music.set_volume(0.4)
    quadrapassel_app = NoticeWindow()
    sys.exit(app.exec_())
