import json
import os

from anthropic import Anthropic

from player.llm_player import LLMPlayer
from util import to_string_board, read_file

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")


class ClaudeOpusPlayer(LLMPlayer):
    def get_move(self, board):
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the current state of the board:\n{to_string_board(board)}"
        messages = [
                       {"role": "user", "content": content}
                   ] + self.history
        client = Anthropic(api_key=CLAUDE_API_KEY)
        response = client.messages.create(
            temperature=1.0,
            model="claude-3-opus-20240229",
            max_tokens=3000,
            messages=messages
        )
        json_response = json.loads(response.content[0].text)
        return json_response['x'], json_response['y'], json_response['reason']
