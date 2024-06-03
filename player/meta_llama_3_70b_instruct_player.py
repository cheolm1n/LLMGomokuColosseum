import json

import boto3

from player.llm_player import LLMPlayer
from record import Record
from util import read_file, convert_kifu_to_coord


class MetaLlamaThree70BInstructPlayer(LLMPlayer):
    model_id = 'meta.llama3-70b-instruct-v1:0'  # Llama 3 70B Instruct 모델 ID
    accept = 'application/json'
    content_type = 'application/json'

    boto = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')  # AWS 클라이언트 생성

    def get_move(self, record: Record):
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the history of the game (There is no history in the first move):\n{record.to_kifu()}"
        messages = [
            {"role": "user", "content": content}
        ]
        body = json.dumps({
            "prompt": self.__convert_messages_to_llama_prompt(messages),
            "max_gen_len": 2048,
            "temperature": 1.0
        })

        response = self.boto.invoke_model(body=body, modelId=self.model_id, accept=self.accept, contentType=self.content_type)
        json_response = json.loads(json.loads(response.get('body').read()).get('generation'))
        return *convert_kifu_to_coord(json_response['position']), json_response['reason']

    @staticmethod
    def __convert_messages_to_llama_prompt(messages):
        prompt = "<|begin_of_text|>"
        for message in messages:
            if message["role"] == "user":
                prompt += f"\n<|start_header_id|>user<|end_header_id|>\n{message['content']}\n<|eot_id|>\n"
            elif message["role"] == "assistant":
                prompt += f"\n<|start_header_id|>assistant<|end_header_id|>\n{message['content']}\n<|eot_id|>\n"
        prompt += f"\n<|start_header_id|>assistant<|end_header_id|>\n"
        return prompt.strip()
