import json
from uuid import uuid4

import numpy as np

from util import print_board


# 현재 보드 상태에서 승자를 판단합니다.
def check_winner(board, player):
    # 가로, 세로, 대각선 체크
    for i in range(15):
        for j in range(11):
            if all(board[i, j:j + 5] == player) or all(board[j:j + 5, i] == player):
                return True
            if i <= 10 and j <= 10 and all(board[i + k, j + k] == player for k in range(5)):
                return True
            if i >= 4 and j <= 10 and all(board[i - k, j + k] == player for k in range(5)):
                return True
    return False


# 게임을 진행합니다.
def play_game(player1, player2):
    board = np.zeros((15, 15), dtype=int)
    current_player = player1
    move_count = 0
    retry_count = 0
    while move_count < 15 * 15:
        x, y = current_player.get_move(board)
        if board[x, y] == 0:
            board[x, y] = current_player.player_number
            move_count += 1
            print(f"\nPlayer {current_player.player_number} move:")
            print_board(board)
            if check_winner(board, current_player.player_number):
                print(f"Player {current_player.player_number} wins!")
                return current_player.player_number
            current_player = player2 if current_player == player1 else player1
            current_player.history = []  # Clear history for the next player
            retry_count = 0
        else:
            retry_count += 1
            print(f"Invalid move, {retry_count} try again.")
            if retry_count >= 3:
                print("3번 착수에 실패하여 다른 플레이어턴으로 넘어갑니다.")
                current_player = player2 if current_player == player1 else player1
                retry_count = 0
                current_player.history.clear()
            invalid_move = json.dumps("{'x': " + f"{x}" + ", 'y': " + f"{y}" + "}")
            current_player.add_history({"role": "assistant", "content": f"{invalid_move}"})
            current_player.add_history({"role": "user",
                                        "content": "You just made a wrong move. Another stone has already been placed there. "
                                                   "You can only place stones where marked 0. "
                                                   "Please move to another location. There is no need for apologies or excuses. "
                                                   "Please respond only with coordinate values in json format."
                                                   "x and y can only take values from 0 to 14."
                                                   "Please move to another location. "
                                        })
