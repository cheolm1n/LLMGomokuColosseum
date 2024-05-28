import json

import numpy as np

from uuid import uuid4

from log.match import MatchLogger, MatchLog
from log.move import MoveLogger, MoveLog
from player.llm_player import LLMPlayer
from record import Record
from util import print_board, get_now_unix_ms, get_color_from_player


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


class Game:
    def __init__(
        self,
        player1: LLMPlayer,
        player2: LLMPlayer
    ):
        self.player1 = player1
        self.player2 = player2
        self.match_logger = None
        self.move_logger = None
        self.record = Record()

    def play(self, log_move=True, log_match=True) -> int:
        # initialize move_logger
        if log_move:
            if not self.move_logger:
                self.move_logger = MoveLogger()
            self.move_logger.clear()

        # initialize match_logger
        if log_match:
            if not self.match_logger:
                self.match_logger = MatchLogger()
            self.match_logger.clear()

        # initialize game
        board = np.zeros((15, 15), dtype=int)
        current_player = self.player1
        move_count = 0
        retry_count = 0

        game_record = Record()

        # start game
        match_id = str(uuid4())
        black = self.player1.__class__.__name__
        white = self.player2.__class__.__name__
        started = get_now_unix_ms()

        while move_count < 15 * 15:
            move_before = get_now_unix_ms()
            x, y = current_player.get_move(board)
            move_after = get_now_unix_ms()
            if board[x, y] == 0:
                board[x, y] = current_player.player_number
                move_count += 1
                print(f"\nPlayer {current_player.player_number} move:")
                print_board(board)

                if log_move:
                    self.move_logger.append_log(
                        MoveLog(
                            match_id=match_id,
                            color=get_color_from_player(current_player),
                            order=move_count,
                            x=x,
                            y=y,
                            time_spent=move_after - move_before,
                            moved=move_after,
                            valid=1,
                            retry_count=retry_count
                        )
                    )
                game_record.add(player=current_player, x=x, y=y, valid=True)
                if check_winner(board, current_player.player_number):
                    print(f"Player {current_player.player_number} wins!")
                    break

                current_player = self.player2 if current_player == self.player1 else self.player1
                current_player.history = []  # Clear history for the next player
                retry_count = 0
            else:
                if log_move:
                    self.move_logger.append_log(
                        MoveLog(
                            match_id=match_id,
                            color=get_color_from_player(current_player),
                            order=move_count,
                            x=x,
                            y=y,
                            time_spent=move_after - move_before,
                            moved=move_after,
                            valid=0,
                            retry_count=retry_count
                        )
                    )
                retry_count += 1
                print(f"Invalid move, {retry_count} try again.")
                if retry_count >= 3:
                    print("3번 착수에 실패하여 다른 플레이어턴으로 넘어갑니다.")
                    current_player = self.player2 if current_player == self.player1 else self.player1
                    retry_count = 0
                    current_player.history.clear()
                    game_record.add(player=current_player, x=-1, y=-1, valid=False)
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

        ended = get_now_unix_ms()
        winner = black if current_player.player_number == self.player1.player_number else white

        if log_match:
            self.match_logger.append_log(
                MatchLog(
                    match_id=match_id,
                    white=white,
                    black=black,
                    started=started,
                    ended=ended,
                    winner=winner
                )
            )

        if log_match:
            self.match_logger.append_to_csv()
        if log_move:
            self.move_logger.append_to_csv()

        return current_player.player_number
