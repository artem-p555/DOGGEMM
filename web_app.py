from flask import Flask, render_template, request, jsonify
from main import main, get_valid_input, update_board, print_board, is_valid_move
import random  # Для случайных ходов бота

app = Flask(__name__)

# Store the state of the game
game_state = {
    "board": None,
    "A": None,
    "player1_pieces": None,
    "player2_pieces": None,
    "player1_count": None,
    "player2_count": None,
    "current_player": None,
    "player2_is_bot": False  # Флаг для второго игрока (бот ли он?)
}

@app.route('/')
def home():
    return render_template('game.html')

@app.route('/start', methods=['POST'])
def start_game():
    global game_state
    data = request.json
    board_size = data.get("board_size", 4)  # Динамический ввод размера доски, по умолчанию 4
    num_players = data.get("num_players", 2)  # Количество игроков
    first_player = data.get("first_player", 1)  # Кто ходит первым
    player2_is_bot = data.get("player2_is_bot", False)  # Флаг для того, чтобы второй игрок был ботом

    # Убедимся, что размер доски корректный
    if board_size < 3 or board_size > 10:
        return jsonify({"message": "Invalid board size! Please choose between 3 and 10."}), 400

    # Инициализация игры
    A = board_size
    player1_pieces = [10 * j + 1 for j in range(1, A)]
    player2_pieces = [10 * A + j + 1 for j in range(1, A)]
    player1_count = A - 1
    player2_count = A - 1

    # Построение доски
    board = [["." for _ in range(A)] for _ in range(A)]
    for j in range(1, A):
        r = int(player1_pieces[j - 1] / 10)
        c = player1_pieces[j - 1] - 10 * r
        board[r - 1][c - 1] = str(j)
    for j in range(1, A):
        r = int(player2_pieces[j - 1] / 10)
        c = player2_pieces[j - 1] - 10 * r
        board[r - 1][c - 1] = chr(64 + j + 1)

    # Обновление состояния игры
    game_state.update({
        "board": board,
        "A": A,
        "player1_pieces": player1_pieces,
        "player2_pieces": player2_pieces,
        "player1_count": player1_count,
        "player2_count": player2_count,
        "current_player": first_player,
        "player2_is_bot": player2_is_bot
    })

    return jsonify({"message": "Game initialized!", "board": board})


@app.route('/move', methods=['POST'])
def make_move():
    global game_state
    data = request.json
    move = data.get("move", "").strip().upper()
    current_player = game_state["current_player"]

    if current_player == 1:
        player_type = "DIGITS"
        pieces = game_state["player1_pieces"]
        piece_count = game_state["player1_count"]
    else:
        player_type = "LETTERS"
        pieces = game_state["player2_pieces"]
        piece_count = game_state["player2_count"]

    if move == "R":
        winner = "LETTERS" if player_type == "DIGITS" else "DIGITS"
        return jsonify({"message": f"{player_type} resigned. {winner} wins!"})

    # Если второй игрок - бот, генерируем его ход
    if current_player == 2 and game_state["player2_is_bot"]:
        move = generate_bot_move(pieces, game_state["board"], player_type)
        if not move:
            return jsonify({"message": "No valid move available for bot."})
        print(f"Bot's move: {move}")  # Выводим ход бота для отладки

    # Calculate the piece index correctly based on the player type
    try:
        piece_index = int(move[0]) - 1 if player_type == "DIGITS" else ord(move[0].upper()) - ord('A') - 1
    except ValueError:
        return jsonify({"message": "Invalid piece. Please provide a valid move!"})

    if not is_valid_move(game_state["board"], game_state["A"], pieces, piece_index, move[1], player_type):
        return jsonify({"message": "Invalid move!"})

    pieces, piece_count = update_board(game_state["board"], game_state["A"], pieces, piece_count, move, player_type)

    if player_type == "DIGITS":
        game_state["player1_pieces"], game_state["player1_count"] = pieces, piece_count
    else:
        game_state["player2_pieces"], game_state["player2_count"] = pieces, piece_count

    if piece_count == 0:
        return jsonify({"message": f"*** {player_type} WIN!!!"})

    game_state["current_player"] = 2 if current_player == 1 else 1
    return jsonify({"board": game_state["board"], "current_player": game_state["current_player"]})


def generate_bot_move(pieces, board, player_type):
    """
    Генерация случайного хода для бота.
    Бот движется в направлениях N (наверх), E (направо), W (налево).
    Исключаем движение на юг (S).
    """
    valid_moves = []
    for i, piece in enumerate(pieces):
        # Получаем строковое представление фигуры (например, "B", "C" и т.д.)
        piece_char = chr(65 + i)  # Преобразуем индекс фигуры в символ буквы

        # Пробуем сгенерировать допустимые ходы для каждой фигуры
        for direction in ["N", "E", "W"]:  # Направления: N (наверх), E (направо), W (налево)
            if is_valid_move(board, game_state["A"], pieces, i, direction, player_type):
                valid_moves.append(f"{piece_char}{direction}")

    if valid_moves:
        return random.choice(valid_moves)  # Возвращаем случайный допустимый ход
    return None



if __name__ == '__main__':
    app.run(debug=True)
