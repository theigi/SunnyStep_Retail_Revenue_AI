from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from prompts import SYSTEM_PROMPT
import json, os

load_dotenv()
app=FastAPI(title="SunnyStep Retail Revenue AI")
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RetailRequest(BaseModel):
    retail_data: dict

@app.post("/analyze")
async def analyze(req: RetailRequest):
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type":"json_object"},
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":json.dumps(req.retail_data,indent=2)}
        ]
    )
    return json.loads(response.choices[0].message.content)
