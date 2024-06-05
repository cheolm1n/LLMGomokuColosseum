import json
from typing import Optional

import numpy as np

from uuid import uuid4
from datetime import datetime

from log.match import MatchLogger, MatchLog
from log.move import MoveLogger, MoveLog
from player.llm_player import LLMPlayer
from record import Record
from util import print_board, get_now_unix_ms, get_color_from_player, convert_coord_to_kifu, InvalidPositionException, get_stone


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
        self.record = Record()

    async def play(self, name: Optional[str] = None) -> LLMPlayer:
        if name:
            filename = name
        else:
            filename = datetime.now().strftime('%Y%m%d%H%M%S')

        with MoveLogger(filename) as move_logger, MatchLogger(filename) as match_logger:
            return await self.__play_game(move_logger=move_logger, match_logger=match_logger)

    async def __play_game(self, move_logger: MoveLogger, match_logger: MatchLogger) -> LLMPlayer:
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
            position_valid = True

            try:
                x, y, position, reason, geval_score, geval_reason = await current_player.get_move(game_record)
                if board[x, y] > 0:
                    position_valid = False
            except (InvalidPositionException, KeyError):
                position_valid = False

            move_after = get_now_unix_ms()

            if position_valid:
                board[x, y] = current_player.player_number
                move_count += 1
                stone = get_stone(current_player)
                print(f"\nPlayer {current_player.player_number}({stone}) move : {convert_coord_to_kifu(x=x, y=y)}, reason : {reason}")
                print_board(board, (x, y), current_player.player_number)

                move_logger.append_log(
                    MoveLog(
                        match_id=match_id,
                        color=get_color_from_player(current_player),
                        order=move_count,
                        time_spent=move_after - move_before,
                        moved=move_after,
                        valid=1,
                        retry_count=retry_count,
                        x=x,
                        y=y,
                        position=position,
                        reason=reason,
                        geval_score=geval_score,
                        geval_reason=geval_reason
                    )
                )
                game_record.add(player=current_player, x=x, y=y, valid=True, reason=reason)
                if check_winner(board, current_player.player_number):
                    print(f"Player {current_player.player_number}({stone}) wins!")
                    break

                current_player = self.player2 if current_player == self.player1 else self.player1
                current_player.history = []  # Clear history for the next player
                retry_count = 0
            else:
                move_logger.append_log(
                    MoveLog(
                        match_id=match_id,
                        color=get_color_from_player(current_player),
                        order=move_count,
                        time_spent=move_after - move_before,
                        moved=move_after,
                        valid=0,
                        retry_count=retry_count,
                        x=x,
                        y=y,
                        position=position,
                        reason=reason,
                        geval_score=geval_score,
                        geval_reason=geval_reason
                    )
                )
                retry_count += 1
                print(f"Invalid move, {retry_count} try again.")
                if retry_count >= 3:
                    print("3번 착수에 실패하여 다른 플레이어턴으로 넘어갑니다.")
                    current_player = self.player2 if current_player == self.player1 else self.player1
                    retry_count = 0
                    current_player.history.clear()
                    game_record.add(player=current_player, x=-1, y=-1, valid=False, reason=None)
                current_player.add_history({"role": "assistant", "content": json.dumps({'position': convert_coord_to_kifu(x=x, y=y), "reason": reason})})
                current_player.add_history({"role": "user",
                                            "content": "You just made a wrong move. Another stone has already been placed there. "
                                                       "You can only place stones where not presented before. "
                                                       "Please move to another location. There is no need for apologies or excuses. "
                                                       "Please respond only with Kifu notation in json format like {\"position\": \"F10\", \"reason\":\"# Current Sequences: Player 1 has a "
                                                       "horizontal sequence from F8 to I8. By placing a stone at E8, I can further extend the horizontal sequence and create a strong threat. # "
                                                       "Winning Move: Continue building the horizontal sequence from F8 to I8 by placing a stone at E8. # Best Move: E8 # Reason: Extending the "
                                                       "horizontal sequence increases the chances of creating a winning pattern in the future.\"}."
                                                       "Alphabet(as columns) is in between A from O. and number(as rows) is in between 1 from 15."
                                                       "Please move to another location. "
                                            })

        ended = get_now_unix_ms()
        winner = black if current_player.player_number == self.player1.player_number else white

        geval_avg_total, geval_avg_black, geval_avg_white = move_logger.get_geval_average()
        match_logger.append_log(
            MatchLog(
                match_id=match_id,
                white=white,
                black=black,
                started=started,
                ended=ended,
                winner=winner,
                geval_avg_total=geval_avg_total,
                geval_avg_black=geval_avg_black,
                geval_avg_white=geval_avg_white
            )
        )

        return current_player

