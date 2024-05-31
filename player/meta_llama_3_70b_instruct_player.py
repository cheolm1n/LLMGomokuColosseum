import json

from friendli import Friendli

from player.llm_player import LLMPlayer
from record import Record
from util import to_string_board, read_file, convert_kifu_to_coord


class MetaLlamaThree70BInstructPlayer(LLMPlayer):
    def get_move(self, record: Record):
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the history of the game (There is no history in the first move):\n{record.to_kifu()}"
        messages = [
            {"role": "user", "content": content}
        ]
        client = Friendli()

        response = client.chat.completions.create(
            model="meta-llama-3-70b-instruct",
            messages=messages,
            temperature=1.0,
            max_tokens=3000,
            stream=False,
        )

        json_response = json.loads(response.choices[0].message.content)
        return *convert_kifu_to_coord(json_response['position']), json_response['reason']
