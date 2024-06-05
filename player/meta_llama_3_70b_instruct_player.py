import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

import boto3

from player.llm_player import LLMPlayer
from record import Record
from util import read_file, convert_kifu_to_coord


class MetaLlamaThree70BInstructPlayer(LLMPlayer):
    def __init__(self, player_number, is_evaluate=False):
        super().__init__(player_number)
        self.is_evaluate = is_evaluate

    model_id = 'meta.llama3-70b-instruct-v1:0'  # Llama 3 70B Instruct 모델 ID
    accept = 'application/json'
    content_type = 'application/json'

    boto = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')  # AWS 클라이언트 생성

    async def get_move(self, record: Record):
        prompt = read_file("gomoku_prompt.txt")
        content = f"{prompt}\nYou are playing with stone '{self.player_number}'.\nYour turn. Here is the history of the game (There is no history in the first move):\n{record.get_kifu_for(self.player_number)}"
        messages = [
            {"role": "user", "content": content}
        ]
        body = json.dumps({
            "prompt": self.__convert_messages_to_llama_prompt(messages),
            "max_gen_len": 2048,
            "temperature": 1.0
        })

        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            response = await loop.run_in_executor(pool, self.__invoke_model_sync, body)

        json_response = json.loads(json.loads(response.get('body').read()).get('generation'))
        position = json_response['position']

        geval_score, geval_reason = {0, ""}
        if self.is_evaluate:
            geval_score, geval_reason = self.gen_evaluate(json.dumps(messages), json_response)

        return *convert_kifu_to_coord(position), position, json_response['reason'], geval_score, geval_reason

    def __invoke_model_sync(self, body: str):
        return self.boto.invoke_model(body=body, modelId=self.model_id, accept=self.accept, contentType=self.content_type)

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
