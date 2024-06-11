import json
import os
import typing

import google.generativeai as genai
from google.generativeai.types import generation_types

from player.llm_player import LLMPlayer
from record import Record
from util import convert_string_format, read_file, to_string_board, convert_kifu_to_coord

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


class GoogleGeminiProPlayer(LLMPlayer):
    def __init__(self, player_number, is_evaluate=False):
        super().__init__(player_number)
        self.is_evaluate = is_evaluate

    async def get_move(self, record: Record):
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the history of the game (There is no history in the first move):\n{record.get_kifu_for(self.player_number)}"

        messages = [
            {
                "role": "user",
                "parts": [content + convert_string_format(self.history), "Response with ONLY JSON format. Do not include control characters or backquotes in your response."]
            },
            {
                "role": "model",
                "parts": '{"'
            }
        ]

        response = await model.generate_content_async(messages,
                                          generation_config=genai.types.GenerationConfig(
                                              candidate_count=1,
                                              temperature=1.0,
                                          ))

        response_text = '{"' + response.text if not response.text.startswith('{"') else response.text
        json_response = json.loads(response_text)
        position = json_response['position']

        geval_score, geval_reason = None, None
        if self.is_evaluate:
            geval_score, geval_reason = self.gen_evaluate(json.dumps(messages), json_response)

        return *convert_kifu_to_coord(position), position, json_response['reason'], geval_score, geval_reason
