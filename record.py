from dataclasses import dataclass

from player.llm_player import LLMPlayer
from util import get_color_from_player, BOARD_COLUMNS, convert_coord_to_kifu


@dataclass
class RecordHistory:
    player: LLMPlayer
    x: int
    y: int
    valid: bool

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

    def add(self, player: LLMPlayer, x: int, y: int, valid: bool):
        self.history.append(
            RecordHistory(player=player, x=x, y=y, valid=valid)
        )

    def to_kifu(self, joiner=" ") -> str:
        """
        convert to kifu record.
        INVALID is invalid move (not standard notation)
        ex)
        A3 B4 C5
        """
        return joiner.join([history.get_kifu_position() for history in self.history])
