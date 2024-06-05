import json
import os

from openai import AsyncOpenAI

from player.llm_player import LLMPlayer
from record import Record
from util import read_file, to_string_board, convert_kifu_to_coord

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class OpenAiGptFourOmniPlayer(LLMPlayer):
    def __init__(self, player_number, is_evaluate=False):
        super().__init__(player_number)
        self.is_evaluate = is_evaluate

    async def get_move(self, record: Record):
        prompt = read_file("gomoku_prompt.txt")
        messages = [
                       {"role": "system", "content": prompt},
                       {"role": "user", "content": f"You are playing with stone '{self.player_number}'.\nYour turn. Here is the history of the game (There is no history in the first move):\n{record.get_kifu_for(self.player_number)}"}
                   ] + self.history
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1.0,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )
        json_response = json.loads(response.choices[0].message.content.strip())
        position = json_response['position']

        geval_score, geval_reason = {0, ""}
        if self.is_evaluate:
            geval_score, geval_reason = self.gen_evaluate(json.dumps(messages), json_response)
            print(f"geval_score:{geval_score}, geval_reason:{geval_reason}")

        return *convert_kifu_to_coord(position), position, json_response['reason'], geval_score, geval_reason
