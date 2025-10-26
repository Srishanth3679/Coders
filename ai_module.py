from fastapi import FastAPI, Body, HTTPException
from openai import OpenAI
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 
@app.post("/ai-review/")
async def ai_review(code: str = Body(..., embed=True)):
if not code:
raise HTTPException(status_code=400, detail="No code provided.")
try:
response = client.chat.completions.create(
model="gpt-4o",  # replace with available model
messages=[
{"role": "system", "content": "You are a senior AI code reviewer."},
{"role": "user", "content": f"Please review this code and suggest improvements:\n{code}"}
]
)
return {"review": response.choices[0].message.content}
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))
  
