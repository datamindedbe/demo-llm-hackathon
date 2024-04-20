import boto3

ssm_client = boto3.client('ssm', region_name='eu-west-1')


BEDROCK_BUCKET = 'llmhackathon-demo'
BEDROCK_REGION ='us-east-1'
BEDROCK_KNOWLEDGE_BASE_ID ='ECZYEUIJ59'
OPENAI_API_KEY = ssm_client.get_parameter(Name='llm-hackathon-openai-key')['Parameter']['Value']
OPENAI_MODEL_NAME = 'gpt-4-turbo'