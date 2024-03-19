from openai import OpenAI
import os

api_key = os.getenv("API_KEY")

def generate_description(brand: str, model:str, specifications: dict):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user",
         "content": f"Imagine, that you are describing camera to a customer"
                    f" to sell it. do not include your personal experience with camera"
                    f" and provide a concise and brief description of it."
                    f"brand: {brand}\nmodel:{model}\nspecifications:{specifications}"}
      ]
    )

    return dict(completion.choices[0].message)['content']
