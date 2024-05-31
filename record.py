from dataclasses import dataclass
from typing import Optional

from player.llm_player import LLMPlayer
from util import get_color_from_player, BOARD_COLUMNS, convert_coord_to_kifu


@dataclass
class RecordHistory:
    player: LLMPlayer
    x: int
    y: int
    valid: bool
    reason: str

    @property
    def color(self):
        return get_color_from_player(self.player)

    def get_kifu_position(self): # 15 * 15 board
        if self.valid:
            return convert_coord_to_kifu(x=self.x, y=self.y)
        else:
            # not standard notation
            return "INVALID"


class Record:
    def __init__(self):
        self.history: list[RecordHistory] = []

    def add(self, player: LLMPlayer, x: int, y: int, valid: bool, reason: Optional[str]):
        self.history.append(
            RecordHistory(player=player, x=x, y=y, valid=valid, reason=reason)
        )

    def to_kifu(self, joiner="\n") -> str:
        """
        convert to kifu record.
        INVALID is invalid move (not standard notation)
        ex)
        A3 B4 C5
        """
        return joiner.join([
            f'player {history.player.player_number}: {history.get_kifu_position()} (reason: {history.reason})'
            for history in self.history
        ])
