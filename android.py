import random
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock

class DodgeGameApp(App):
    def build(self):
        self.board_size = 5  # Размер доски по умолчанию
        self.board = []
        self.player1_pieces = []  # Список фишек игрока 1
        self.player2_pieces = []  # Список фишек игрока 2

        self.layout = BoxLayout(orientation="vertical")

        # Кнопка для начала игры
        self.start_game_button = Button(text="Начать игру", size_hint=(1, None), height=40)
        self.start_game_button.bind(on_press=self.choose_board_size)
        self.layout.add_widget(self.start_game_button)

        # Кнопка для отображения инструкций
        self.instructions_button = Button(text="Инструкции", size_hint=(1, None), height=40)
        self.instructions_button.bind(on_press=self.show_instructions)
        self.layout.add_widget(self.instructions_button)

        return self.layout

    def choose_board_size(self, instance):
        # Окно выбора размера доски
        content = BoxLayout(orientation="vertical")
        size_spinner = Spinner(
            text='5',
            values=[str(i) for i in range(3, 11)],
            size_hint=(None, None),
            size=(200, 44)
        )
        content.add_widget(Label(text="Выберите размер доски:"))
        content.add_widget(size_spinner)

        start_button = Button(text="Начать", size_hint=(1, None), height=40)
        content.add_widget(start_button)

        popup = Popup(title='Настройка игры', content=content, size_hint=(None, None), size=(300, 300))

        def start_game(instance):
            self.board_size = int(size_spinner.text)
            self.initialize_game()
            popup.dismiss()

        start_button.bind(on_press=start_game)
        popup.open()

    def initialize_game(self):
        # Создаём игровую доску и фишки
        self.board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.player1_pieces = [str(i) for i in range(1, self.board_size)]
        self.player2_pieces = [chr(65 + i) for i in range(self.board_size - 1)]

        # Распределяем фишки по доске
        for i, piece in enumerate(self.player1_pieces):
            self.board[i][0] = piece  # Цифры (игрок 1) в первом столбце
        for i, piece in enumerate(self.player2_pieces):
            self.board[self.board_size - 1][i + 1] = piece  # Буквы (игрок 2) в последнем ряду

        self.layout.clear_widgets()

        # Сетка игрового поля
        self.board_layout = GridLayout(cols=self.board_size, rows=self.board_size, size_hint=(1, None))
        self.board_layout.height = self.board_size * 40
        self.update_board()
        self.layout.add_widget(self.board_layout)

        # Поле для ввода хода
        input_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=40)
        self.move_input = TextInput(hint_text="Введите ход (пример: 1E или BE)", multiline=False)
        make_move_button = Button(text="Сделать ход")
        make_move_button.bind(on_press=self.make_move)
        input_layout.add_widget(self.move_input)
        input_layout.add_widget(make_move_button)

        self.layout.add_widget(input_layout)

        # Кнопка для завершения игры
        quit_button = Button(text="Закончить игру", size_hint=(1, None), height=40)
        quit_button.bind(on_press=self.show_victory_popup)
        self.layout.add_widget(quit_button)

        # Сообщение о текущем игроке
        self.current_player_label = Label(text="Ходит: Игрок 1 (Цифры)", size_hint=(1, None), height=40)
        self.layout.add_widget(self.current_player_label)

        self.current_player = 1  # Игрок 1 начинает первым

    def update_board(self):
        # Обновление отображения доски
        self.board_layout.clear_widgets()
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = Button(text=self.board[i][j], size_hint=(None, None), width=40, height=40)
                self.board_layout.add_widget(cell)

    def show_instructions(self, instance):
        instructions = """
        В этой игре два игрока перемещают свои фишки по доске:
        Игрок 1 (цифры):
          - 1E: вправо
          - 1S: вниз
          - 1N: вверх
        Игрок 2 (буквы):
          - BE: вправо
          - BW: влево
          - BN: вверх
        Побеждает тот, кто достигнет своей цели:
          - Игрок 1: цифры достигают правого края.
          - Игрок 2: буквы достигают верхнего края.
        """
        popup = Popup(title='Инструкции', content=Label(text=instructions), size_hint=(None, None), size=(400, 400))
        popup.open()

    def make_move(self, instance):
        move_text = self.move_input.text.strip()
        if not move_text:
            return

        try:
            player, direction = move_text[0], move_text[1:]
            if self.current_player == 1 and player.isdigit():
                self.move_player1(player, direction)
            elif self.current_player == 2 and player.isalpha() and player in self.player2_pieces:
                self.move_player2(player, direction)
            else:
                self.show_error("Неверный ход. Сейчас ходит игрок " + ("1 (Цифры)" if self.current_player == 1 else "2 (Буквы)"))
            self.check_victory()
            self.switch_player()
        except Exception:
            self.show_error("Некорректный формат. Пример: '1E' или 'BE'.")
        finally:
            self.move_input.text = ""

    def move_player1(self, piece, direction):
        # Перемещение фишек игрока 1
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == piece:
                    new_i, new_j = i, j
                    if direction == 'E' and j < self.board_size - 1:
                        new_j += 1
                    elif direction == 'S' and i < self.board_size - 1:
                        new_i += 1
                    elif direction == 'N' and i > 0:
                        new_i -= 1
                    else:
                        continue

                    if self.board[new_i][new_j] == '.':
                        self.board[i][j], self.board[new_i][new_j] = '.', piece
                        self.update_board()
                        return

    def move_player2(self, piece, direction):
        # Перемещение фишек игрока 2
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == piece:
                    new_i, new_j = i, j
                    if direction == 'E' and j < self.board_size - 1:
                        new_j += 1
                    elif direction == 'W' and j > 0:
                        new_j -= 1
                    elif direction == 'N' and i > 0:
                        new_i -= 1
                    else:
                        continue

                    if self.board[new_i][new_j] == '.':
                        self.board[i][j], self.board[new_i][new_j] = '.', piece
                        self.update_board()
                        return

    def check_victory(self):
        # Проверяем, достигли ли все цифры правого края
        if all(self.board[i][self.board_size - 1] in self.player1_pieces for i in range(self.board_size)):
            self.show_victory_popup("Цифры победили!")
        # Проверяем, достигли ли все буквы верхнего края
        elif all(self.board[0][j] in self.player2_pieces for j in range(1, self.board_size)):
            self.show_victory_popup("Буквы победили!")

    def show_victory_popup(self, message):
        # Создаём окно с сообщением о победе и кнопкой переиграть
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text=message))
        replay_button = Button(text="Переиграть", size_hint=(1, None), height=40)
        replay_button.bind(on_press=self.replay_game)
        content.add_widget(replay_button)

        popup = Popup(title='Победитель', content=content, size_hint=(None, None), size=(400, 300))
        popup.open()

    def show_error(self, message):
        popup = Popup(title='Ошибка', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def switch_player(self):
        # Переключаем игрока
        self.current_player = 2 if self.current_player == 1 else 1
        self.current_player_label.text = "Ходит: Игрок " + str(self.current_player) + " (" + ("Цифры)" if self.current_player == 1 else "Буквы)")

    def replay_game(self, instance):
        self.initialize_game()  # Сброс игры и инициализация

if __name__ == '__main__':
    DodgeGameApp().run()
