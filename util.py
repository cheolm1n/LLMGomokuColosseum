from time import time

from player.llm_player import LLMPlayer


BOARD_COLUMNS = list("ABCDEFGHIJKLMNO")

# 보드 상태를 문자열로 변환 합니다.
def to_string_board(board):
    result = "```\n"
    for row in board:
        result += "".join('1' if x == 1 else '2' if x == 2 else '0' for x in row)
        result += "\n"
    result += "```\n"
    return result


# 보드 상태를 사람이 보기 좋게 변환 합니다.
def print_board(board):
    for row in board:
        print(" ".join('●' if x == 1 else '○' if x == 2 else '·' for x in row))


# 파일을 읽어옵니다.
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return ""


# 데이터 포맷을 변환합니다. (구글 제미나이 응답에 맞춰)
def convert_data_format(data_as_is):
    return [{"role": item["role"] if item["role"] == "user" else "model", "parts": item["content"]} for item in data_as_is]


# 문자열 포맷을 변환합니다. (구글 제미나이 응답에 맞춰)
def convert_string_format(data_as_is):
    return ''.join([item["content"] for item in data_as_is])


def get_now_unix_ms():
    return round(time() * 1000)


def get_color_from_player(player: LLMPlayer) -> str:
    return "black" if player.player_number == 1 else "white"


def convert_kifu_to_coord(position: str) -> tuple[int, int]:
    if len(position) != 2 and len(position) != 3:
        raise ValueError(f"Position not valid: {position}")

    position_col, position_row = position[:1], position[1:]
    if position_col not in BOARD_COLUMNS or not (1 <= int(position_row) <= 15):
        raise ValueError(f"Position not valid: {position}")

    return int(position_row) - 1, BOARD_COLUMNS.index(position_col)


def convert_coord_to_kifu(x: int, y: int) -> str:
    return f"{BOARD_COLUMNS[y]}{x + 1}"
