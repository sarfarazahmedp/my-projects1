"""Set GEMINI_API_KEY, then run: uvicorn app:app --reload"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai

app = FastAPI(title="AI Study Assistant")

class Question(BaseModel):
    message: str

PAGE = """<!doctype html><title>AI Study Assistant</title><style>body{max-width:720px;margin:60px auto;padding:0 20px;font:17px system-ui;background:#f5f1e9;color:#161616}textarea,button{box-sizing:border-box;width:100%;padding:14px;font:inherit;margin-top:12px}button{background:#e65426;border:2px solid #161616;font-weight:bold;cursor:pointer}#answer{white-space:pre-wrap;line-height:1.6;margin-top:28px}</style><h1>AI Study Assistant</h1><p>Ask for an explanation, example, or study plan.</p><textarea id=q rows=5 placeholder="Explain Python decorators simply..."></textarea><button onclick=ask()>Ask assistant</button><div id=answer></div><script>async function ask(){let a=document.querySelector('#answer');a.textContent='Thinking…';let r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q.value})});let d=await r.json();a.textContent=d.answer||d.detail}</script>"""

@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE

@app.post("/ask")
def ask(question: Question):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise HTTPException(500, "Set GEMINI_API_KEY before running the assistant.")
    client = genai.Client(api_key=key)
    prompt = "You are a concise, encouraging study assistant. Use examples when useful.\n\n" + question.message
    answer = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"answer": answer.text}
