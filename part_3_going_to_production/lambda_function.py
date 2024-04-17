import json
from typing import Optional
import os
import boto3
import openai


def retrieve(bedrock_client, knowledge_base_id, search_string, items=10):
    retrievals = bedrock_client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={
            'text': search_string
        },
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': items
            }
        }
    )
    return retrievals['retrievalResults']

def get_response(client, prompt:str, model)->str:
    api_response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    return api_response.choices[0].message.content

def lambda_handler(event: dict, context: Optional[dict] = None):
    # basic implementation to test that the connections work

    if 'AWS_PROFILE' in os.environ:
        boto3.setup_default_session(profile_name=os.environ['AWS_PROFILE'])

    query = event["query"]
    bedrock = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    knowledge_base_id = os.environ.get('KNOWLEDGE_BASE_ID')
    retrievals = retrieve(bedrock, knowledge_base_id, query, 5)

    openai_key = os.environ.get('OPENAI_KEY')
    client = openai.OpenAI(api_key=openai_key)
    model_response = get_response(client, query, "gpt-3.5-turbo")


    s3_client= boto3.client('s3')
    s3_content = s3_client.get_object(Bucket='llmhackathon-demo', Key='data/translated/2024/03/en.2024-03-08-mededeling-16ef3a54-da36-11ee-8ea1-ff993de5bafc.txt')
    s3_content = s3_content['Body'].read().decode('utf-8')

    full_response = json.dumps({"test_bedrock":retrievals,"test_openai":model_response, 'test_s3':s3_content})
    return {"statusCode": 200, "body": full_response}
    

if __name__ == "__main__":
    response = lambda_handler({
            "query": "what is the government doing to improve the housing market?"
        }
    )
    print(response)