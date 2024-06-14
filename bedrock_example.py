import boto3
import os
import json

# 환경 변수 설정
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

# AWS 클라이언트 생성
boto = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')


# Claude 3 Opus 모델로 인퍼런스 수행 예제
def infer_claude3_opus(messages):
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": messages}],
            }
        ],
    })
    model_id = 'anthropic.claude-3-opus-20240229-v1:0'  # Claude 3 Opus 모델 ID
    accept = 'application/json'
    content_type = 'application/json'

    response = boto.invoke_model(body=body, modelId=model_id, accept=accept, contentType=content_type)
    response_body = json.loads(response.get('body').read())
    return response_body.get('content')[0]['text']


# Llama 3 70B Instruct 모델로 인퍼런스 수행 예제
def infer_llama3_70b(messages):
    body = json.dumps({
        "prompt": messages,
        "max_gen_len": 512,
        "temperature": 0.5,
    })
    model_id = 'meta.llama3-70b-instruct-v1:0'  # Llama 3 70B Instruct 모델 ID
    accept = 'application/json'
    content_type = 'application/json'

    response = boto.invoke_model(body=body, modelId=model_id, accept=accept, contentType=content_type)
    response_body = json.loads(response.get('body').read())
    return response_body.get('generation')


# 인퍼런스 수행 예제
prompt = "Explain the theory of relativity in simple terms."
claude3_result = infer_claude3_opus(prompt)
llama3_result = infer_llama3_70b(prompt)

print("Claude 3 Opus Response:")
print(claude3_result)

print("\nLlama 3 70B Instruct Response:")
print(llama3_result)
