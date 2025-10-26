from fastapi import FastAPI, Body
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key="YOUR_API_KEY_HERE")

@app.post("/review")
async def review_code(code: str = Body(..., embed=True)):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": f"Review this code and suggest fixes:\n{code}"}
        ]
    )
    return {"review": response.choices[0].message.content}