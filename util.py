from time import time

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
