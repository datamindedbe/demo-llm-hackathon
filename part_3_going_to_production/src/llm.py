from typing import Optional
import openai
from src.config import OPENAI_API_KEY, OPENAI_MODEL_NAME
from src.bedrock import BedrockRetrievedItem

client = openai.OpenAI(
    api_key=OPENAI_API_KEY
)


def get_response(prompt:str)->str:
    api_response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=OPENAI_MODEL_NAME,
    )
    return api_response.choices[0].message.content




def decisions_query(query:str, decisions:list[BedrockRetrievedItem])->str:
    flat_items = [f"{index} : {item.text}" for index, item in enumerate(decisions)]
    flat_items = "\n".join(flat_items)
    prompt = f"""
                Answer the given question using only the information in the sources section below.
                Respond in a conversational manner, not with a list.
                Enter the index number of the source used between single square brackets, such as [1] or [2][3][4].
                do not combine references together in one bracket

                question:{query}
                sources: {flat_items}
                your answer:
    """
    return get_response(prompt)
    