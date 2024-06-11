import json
import os

from anthropic import AsyncAnthropic

from player.llm_player import LLMPlayer
from record import Record
from util import to_string_board, read_file, convert_kifu_to_coord

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")


class ClaudeOpusPlayer(LLMPlayer):
    def __init__(self, player_number, is_evaluate=False):
        super().__init__(player_number)
        self.is_evaluate = is_evaluate

    async def get_move(self, record: Record):
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the history of the game (There is no history in the first move):\n{record.get_kifu_for(self.player_number)}"
        messages = [
                        {"role": "user", "content": content},
                        {"role": "assistant", "content": "{"}
                    ]
        client = AsyncAnthropic(api_key=CLAUDE_API_KEY)

        response = await client.messages.create(
            temperature=1.0,
            model="claude-3-opus-20240229",
            max_tokens=3000,
            messages=messages
        )

        response_text = response.content[0].text
        json_response = json.loads("{" + response_text if not response_text.startswith("{") else response_text)
        position = json_response['position']

        geval_score, geval_reason = None, None
        if self.is_evaluate:
            geval_score, geval_reason = self.gen_evaluate(json.dumps(messages), json_response)

        return *convert_kifu_to_coord(position), position, json_response['reason'], geval_score, geval_reason
