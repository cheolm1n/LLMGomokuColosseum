import json
import os

import google.generativeai as genai

from player.llm_player import LLMPlayer
from util import convert_string_format, read_file, to_string_board

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


class GoogleGeminiProPlayer(LLMPlayer):
    def get_move(self, board):
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the current state of the board:\n{to_string_board(board)}"
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

        response = model.generate_content(messages,
                                          generation_config=genai.types.GenerationConfig(
                                              candidate_count=1,
                                              temperature=1.0)
                                          )
        json_response = json.loads(response.text)
        return json_response['x'], json_response['y']
