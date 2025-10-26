import os
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ 1️⃣ Simple Review Endpoint
@app.post("/review")
async def review_code(code: str = Body(..., embed=True)):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a code reviewer."},
                {"role": "user", "content": f"Review this code and suggest fixes:\n{code}"}
            ]
        )
        return {"review": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Pydantic Request Model
class ReviewRequest(BaseModel):
    code: str

# ✅ 2️⃣ Better AI Review Endpoint
@app.post("/ai-review")
async def ai_review(review: ReviewRequest):
    if not review.code:
        raise HTTPException(status_code=400, detail="No code provided.")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a senior AI code reviewer."},
                {"role": "user", "content": f"Please review this code and suggest improvements:\n{review.code}"}
            ]
        )
        return {"review": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
