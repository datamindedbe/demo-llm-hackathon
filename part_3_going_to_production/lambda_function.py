import json
import boto3
from typing import Optional
from src.bedrock import BedrockRetrievedItem, retrieve_bedrock_items
from src.util import re_reference
from src.llm import decisions_query


def lambda_handler(event: dict, context: Optional[dict] = None):
    # basic implementation to test that the connections work

    body = json.loads(event["body"])
    query = body['query']

    decisions = retrieve_bedrock_items(query, 5)
    llm_response = decisions_query(query, decisions)

    re_referenced_response, used_decisions = re_reference(llm_response, decisions)

    used_decisions_dicts = []
    for decision in used_decisions:
        used_decisions_dicts.append({
            "text": decision.text,
            "decision_url": decision.decision_url,
            "title": decision.title,
            "meeting_date": decision.meeting_date,
            "score": decision.score
        })

    response = json.dumps({"response":re_referenced_response,"decisions":used_decisions_dicts})
    return {"statusCode": 200, "body": response}
    

if __name__ == "__main__":

    input = {
        "body": "{\n    \"query\":\"what is the government doing for parents\"\n}"
    }

    response = lambda_handler(input)
    print(response)