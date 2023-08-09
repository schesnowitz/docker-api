import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_row_col(move):
    return (move - 1) // 3, (move - 1) % 3

def ai_move(board):
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]
    return random.choice(empty_cells) if empty_cells else None

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        
        if current_player == "X":
            move = int(input(f"Player {current_player}, enter your move (1-9): "))
        else:
            print(f"AI ({current_player}) is thinking...")
            move = random.randint(1, 9)

        row, col = get_row_col(move)

        if 1 <= move <= 9 and board[row][col] == " ":
            board[row][col] = current_player

            if check_winner(board, current_player):
                print_board(board)
                if current_player == "X":
                    print(f"Player {current_player} wins!")
                else:
                    print(f"AI ({current_player}) wins!")
                break
            elif is_board_full(board):
                print_board(board)
                print("It's a draw!")
                break

            current_player = "O" if current_player == "X" else "X"
        else:
            print("Invalid move. Try again.")

if __name__ == "__main__":
    main()
