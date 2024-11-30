import random
#game

def main():
    print("DODGEM")
    print("CREATIVE COMPUTING")
    print("MORRISTOWN, NEW JERSEY")
    print("\n" * 3)

    instructions = input("DO YOU WANT INSTRUCTIONS FOR DODGEM? ").strip().lower()
    if instructions.startswith('y'):
        show_instructions()

    board_size = get_valid_input("BOARD SIZE (3-6): ", 3, 6)
    A = board_size

    # Initialize players' pieces
    player1_pieces = [10 * j + 1 for j in range(1, A)]
    player2_pieces = [10 * A + j + 1 for j in range(1, A)]
    player1_count = A - 1
    player2_count = A - 1

    # Initialize board
    board = [["." for _ in range(A)] for _ in range(A)]
    for j in range(1, A):
        r = int(player1_pieces[j - 1] / 10)
        c = player1_pieces[j - 1] - 10 * r
        board[r - 1][c - 1] = str(j)
    for j in range(1, A):
        r = int(player2_pieces[j - 1] / 10)
        c = player2_pieces[j - 1] - 10 * r
        board[r - 1][c - 1] = chr(64 + j + 1)

    num_players = get_valid_input("HOW MANY PLAYERS (1 OR 2): ", 1, 2)
    if num_players == 1:
        first_player = get_valid_input("WHO MOVES FIRST (1=COMPUTER, 2=YOU): ", 1, 2)
    else:
        first_player = 1  # Player 1 starts

    current_player = first_player

    while True:
        print_board(board, A)
        if current_player == 1:
            if num_players == 1 and current_player == 1:
                move = get_computer_move("DIGITS", board, A, player1_pieces, player1_count)
                print(f"DIGITS MOVE: {move}")
            else:
                move = get_player_move("DIGITS", board, A, player1_pieces, player1_count)
            if move == "R":
                print("THE DIGITS GIVE UP!!!")
                print("*** THE LETTERS WIN!!!")
                break
            player1_pieces, player1_count = update_board(board, A, player1_pieces, player1_count, move, "DIGITS")
        else:
            move = get_player_move("LETTERS", board, A, player2_pieces, player2_count)
            if move == "R":
                print("THE LETTERS GIVE UP!!!")
                print("*** THE DIGITS WIN!!!")
                break
            player2_pieces, player2_count = update_board(board, A, player2_pieces, player2_count, move, "LETTERS")

        # Check for win conditions
        if player1_count == 0:
            print("*** THE DIGITS WIN!!!")
            break
        if player2_count == 0:
            print("*** THE LETTERS WIN!!!")
            break

        # Switch players
        current_player = 2 if current_player == 1 else 1


def show_instructions():
    print("\nHERE'S A SAMPLE PLAYING BOARD:")
    print("1 . . . .")
    print("2 . . . .")
    print("3 . . . .")
    print("4 . . . .")
    print(". A B C D")
    print("\nTWO SETS OF PIECES (DIGITS AND LETTERS) RACE ACROSS A SQUARE BOARD.")
    print("DIGITS MOVE EAST TO LEAVE; LETTERS MOVE NORTH TO LEAVE.")
    print("TYPE PIECE AND DIRECTION (e.g., 2E, BW).")
    print("R TO RESIGN, H FOR HELP.\n")


def get_valid_input(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def print_board(board, A):
    for row in board:
        print("  ".join(row))
    print()


def get_player_move(player_type, board, A, pieces, piece_count):
    while True:
        move = input(f"{player_type} MOVE: ").strip().upper()
        if move == "H":
            show_instructions()
            continue
        if move == "R":
            return move
        if len(move) != 2:
            print("Invalid move format. Please try again.")
            continue
        piece = move[0]
        direction = move[1]
        if player_type == "DIGITS":
            if not piece.isdigit() or int(piece) not in range(1, A):
                print("Invalid piece. Please try again.")
                continue
            if direction not in "NES":
                print("Invalid direction. Please try again.")
                continue
        else:
            if not piece.isalpha() or piece not in [chr(64 + j + 1) for j in range(1, A)]:
                print("Invalid piece. Please try again.")
                continue
            if direction not in "NEW":
                print("Invalid direction. Please try again.")
                continue
        return move


def get_computer_move(player_type, board, A, pieces, piece_count):
    while True:
        piece_index = random.randint(0, A - 2)
        piece = str(piece_index + 1) if player_type == "DIGITS" else chr(64 + piece_index + 2)
        directions = "NES" if player_type == "DIGITS" else "NEW"
        direction = random.choice(directions)
        move = piece + direction
        if is_valid_move(board, A, pieces, piece_index, direction, player_type):
            return move


def is_valid_move(board, A, pieces, piece_index, direction, player_type):
    r = int(pieces[piece_index] / 10) - 1
    c = pieces[piece_index] % 10 - 1
    if player_type == "DIGITS":
        if direction == "N" and r > 0 and board[r - 1][c] == ".":
            return True
        elif direction == "E" and c < A - 1 and board[r][c + 1] == ".":
            return True
        elif direction == "S" and r < A - 1 and board[r + 1][c] == ".":
            return True
    else:
        if direction == "N" and r > 0 and board[r - 1][c] == ".":
            return True
        elif direction == "E" and c < A - 1 and board[r][c + 1] == ".":
            return True
        elif direction == "W" and c > 0 and board[r][c - 1] == ".":
            return True
    return False


def update_board(board, A, pieces, piece_count, move, player_type):
    piece = move[0]
    direction = move[1]
    if player_type == "DIGITS":
        piece_index = int(piece) - 1
        r = int(pieces[piece_index] / 10) - 1
        c = pieces[piece_index] % 10 - 1
        if direction == "N" and r > 0 and board[r - 1][c] == ".":
            board[r - 1][c] = piece
            board[r][c] = "."
            pieces[piece_index] -= 10
        elif direction == "E" and c < A - 1 and board[r][c + 1] == ".":
            board[r][c + 1] = piece
            board[r][c] = "."
            pieces[piece_index] += 1
            if c == A - 2:
                piece_count -= 1
        elif direction == "S" and r < A - 1 and board[r + 1][c] == ".":
            board[r + 1][c] = piece
            board[r][c] = "."
            pieces[piece_index] += 10
    else:
        piece_index = ord(piece) - ord('A') - 1
        r = int(pieces[piece_index] / 10) - 1
        c = pieces[piece_index] % 10 - 1
        if direction == "N" and r > 0 and board[r - 1][c] == ".":
            board[r - 1][c] = piece
            board[r][c] = "."
            pieces[piece_index] -= 10
            if r == 1:
                piece_count -= 1
        elif direction == "E" and c < A - 1 and board[r][c + 1] == ".":
            board[r][c + 1] = piece
            board[r][c] = "."
            pieces[piece_index] += 1
        elif direction == "W" and c > 0 and board[r][c - 1] == ".":
            board[r][c - 1] = piece
            board[r][c] = "."
            pieces[piece_index] -= 1
    return pieces, piece_count


if __name__ == "__main__":
    main()
