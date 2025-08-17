# AI-Powered Meeting Notes Summarizer & Sharer

This project is a **full-stack application** that helps teams turn raw meeting transcripts into concise, shareable summaries. Users can upload a transcript file, apply a custom summarization instruction, edit the generated summary, and share it with team members via email.

**Live Link:** https://ai-meeting-summarizer-f2no.onrender.com/
---

## 🚀 Features

- **Transcript Upload**: Supports `.txt` transcript files (with auto-detection of text content)
- **Custom Prompt**: Users can define how the summary should be generated (e.g., *"Summarize in bullet points for executives"*)
- **AI-Powered Summarization**: Uses **Groq API (LLaMA-3.3-70B)** to generate structured summaries
- **Live Editing**: Edit summaries in a markdown editor with real-time preview
- **Email Sharing**: Send final summaries to recipients directly from the app
- **Minimal UI**: Simple and intuitive interface built with Jinja2 templates

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** – Web framework for building APIs and handling requests
- **Groq API (LLaMA 3.3-70B Versatile)** – AI model for summarization
- **SMTP (Gmail)** – For sending email summaries
- **python-dotenv** – For managing environment variables
- **Requests** – For making API calls to Groq
- **Markdown** – Python library for converting Markdown to HTML

### Frontend
- **Jinja2 Templates** – Dynamic HTML rendering
- **Marked.js** – Client-side live Markdown preview
- **Basic CSS** – Minimal styling focused on functionality

---

## 📂 Project Structure

```
├── main.py                    # FastAPI app entry point
├── templates/
│   ├── base.html             # Base template with common styling
│   ├── index.html            # Home page (upload form)
│   └── result.html           # Summary editor with live preview
├── static/
│   └── empty.css             # CSS file (currently empty, can be extended)
├── .env                      # Environment variables (API keys, SMTP credentials)
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/meeting-summarizer.git
cd meeting-summarizer
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```ini
GROQ_API_KEY=your_groq_api_key_here
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

⚠️ **For Gmail, enable "App Passwords" and use it instead of your real password.**

### 5. Run the FastAPI app
```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

---

## 📖 How It Works

### Workflow
1. **Upload a transcript file (.txt) or paste text directly**
2. **Provide an optional prompt** (e.g., "Highlight only action items")
3. **Click Generate Summary** → AI creates a summary
4. **Edit and format the summary** in Markdown
5. **Preview updates live** in the right panel
6. **Enter recipient emails and click Send**

### Key Functions

#### `call_groq_summary(transcript, custom_prompt)`
- Connects to Groq API using LLaMA 3.3-70B model
- Sends transcript with custom instruction
- Returns structured markdown summary

#### `send_email(to_list, subject, html, text)`
- Sends multipart email (HTML + plain text)
- Uses Gmail SMTP with SSL
- Supports multiple recipients

#### `normalize_recipients(raw)`
- Handles comma/semicolon separated email lists
- Cleans and validates recipient addresses

---

## ✅ Future Improvements

- Support for more file formats (.docx, .pdf)
- Authentication & user accounts for team-based use
- Summary history and storage
- Richer formatting and export options (PDF/Word)
- Multiple AI models selection (OpenAI, Claude, Gemini, etc.)
- Real-time collaboration features
- API endpoints for external integrations

---




