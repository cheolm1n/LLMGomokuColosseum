import json
import os

from anthropic import Anthropic

from player.llm_player import LLMPlayer
from record import Record
from util import to_string_board, read_file, convert_kifu_to_coord

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")


class ClaudeOpusPlayer(LLMPlayer):
    def get_move(self, record: Record):
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the history of the game (There is no history in the first move):\n{record.get_kifu_for(self.player_number)}"
        messages = [
                       {"role": "user", "content": content}
                   ]
        client = Anthropic(api_key=CLAUDE_API_KEY)
        response = client.messages.create(
            temperature=1.0,
            model="claude-3-opus-20240229",
            max_tokens=3000,
            messages=messages
        )
        json_response = json.loads(response.content[0].text)
        return *convert_kifu_to_coord(json_response['position']), json_response['reason']
