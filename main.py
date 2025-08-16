import os, textwrap, smtplib
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
from dotenv import load_dotenv
import markdown  # <-- Added for converting markdown to HTML

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")     
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  


def normalize_recipients(raw: str) -> List[str]:
    if not raw:
        return []
    return [x.strip() for x in raw.replace(";", ",").split(",") if x.strip()]


def call_groq_summary(transcript: str, custom_prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    system = "You are an assistant that writes concise meeting summaries in markdown format (bold, lists, headings)."
    user = f"Instruction: {custom_prompt or 'Summarize'}\n\nTranscript:\n{transcript}"

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)
    try:
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}\nResponse: {r.text}"


def send_email(to_list: List[str], subject: str, html: str, text: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_EMAIL
        msg["To"] = ", ".join(to_list)
        msg["Subject"] = subject

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        msg.attach(part1)
        msg.attach(part2)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_list, msg.as_string())

        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/summarize", response_class=HTMLResponse)
async def summarize(
    request: Request,
    transcript: str = Form(""),
    prompt: str = Form(""),
    file: UploadFile = File(None),
):
    text = transcript.strip()
    if file:
        uploaded = (await file.read()).decode("utf-8", errors="ignore")
        text = f"{text}\n\n{uploaded}" if text else uploaded
    if not text:
        return RedirectResponse("/", status_code=303)

    summary = call_groq_summary(text, prompt)
    summary_html = markdown.markdown(summary)  # ✅ Convert markdown to HTML
    return templates.TemplateResponse("result.html", {"request": request, "summary": summary_html, "raw_summary": summary})


@app.post("/send", response_class=HTMLResponse)
async def send(request: Request, summary: str = Form(...), recipients: str = Form(...), subject: str = Form("Meeting Summary")):
    to_list = normalize_recipients(recipients)
    if not to_list:
        return RedirectResponse("/", status_code=303)

    summary_html = markdown.markdown(summary)  # ✅ Convert markdown to HTML
    html = f"<div style='font-family:sans-serif'><h2>Meeting Summary</h2>{summary_html}</div>"
    send_email(to_list, subject, html, summary)
    return RedirectResponse("/", status_code=303)
