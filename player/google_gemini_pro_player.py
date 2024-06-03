import json
import os

import google.generativeai as genai

from player.llm_player import LLMPlayer
from record import Record
from util import convert_string_format, read_file, to_string_board, convert_kifu_to_coord

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


class GoogleGeminiProPlayer(LLMPlayer):
    async def get_move(self, record: Record):
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the history of the game (There is no history in the first move):\n{record.get_kifu_for(self.player_number)}"
        messages = content + convert_string_format(self.history)
        # converted_history = convert_data_format(self.history)
        # messages = ([
        #                {
        #                    "role": "user",
        #                    "parts": content
        #                }
        #            ]
        #             + converted_history
        #             )
        # chat = model.start_chat(history=messages)
        # response = chat.send_message("Now it's your turn.")

        response = await model.generate_content_async(messages,
                                          generation_config=genai.types.GenerationConfig(
                                              candidate_count=1,
                                              temperature=1.0)
                                          )
        json_response = json.loads(response.text)
        return *convert_kifu_to_coord(json_response['position']), json_response['reason']
