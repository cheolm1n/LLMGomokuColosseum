import json
import os

from openai import OpenAI

from player.llm_player import LLMPlayer
from util import read_file, to_string_board

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class OpenAiGptFourOmniPlayer(LLMPlayer):
    def get_move(self, board):
        prompt = read_file("gomoku_prompt.txt")
        messages = [
                       {"role": "system", "content": prompt},
                       {"role": "user", "content": f"You are playing with stone '{self.player_number}'.\nYour turn. Here is the current state of the board:\n{to_string_board(board)}"}
                   ] + self.history
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1.0,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )
        json_response = json.loads(response.choices[0].message.content.strip())
        return json_response['x'], json_response['y'], json_response['reason']
