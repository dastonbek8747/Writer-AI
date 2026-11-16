# AI DOCX Writer

> An AI writing assistant that generates text, evaluates it and exports the result to a Word document. FastAPI backend plus a Streamlit UI.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)


## Features

- Generate a draft on any topic with an LLM.
- Evaluate and improve the draft before export.
- Export the final text to a formatted `.docx` file.
- User accounts with hashed passwords.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| UI | Streamlit |
| LLM | Google Gemini |
| Documents | python-docx |
| Database | SQLAlchemy |
| Packaging | uv (pyproject.toml) |

## Quick Start

```bash
git clone https://github.com/dastonbek8747/ai-docx-writer.git
cd ai-docx-writer
pip install -r requirements.txt
cp .env.example .env      # add your Gemini key and database URL

# terminal 1
uvicorn backend.main:app --reload

# terminal 2
streamlit run app.py
```

## Environment variables

| Variable | Meaning |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key. |
| `DATABASE_URL` | Database connection string. |
| `SECRET_KEY` | Secret used to sign JWTs. |
| `ALGORITHMM` | JWT algorithm, for example `HS256`. |

## Project Structure

```
backend/
├── main.py         # FastAPI app and routes
├── ai_evalutor.py  # LLM generation + evaluation
├── docx_writer.py  # DOCX export
├── hashing.py      # password hashing
├── users.py        # user model
└── db.py           # engine, session, Base
app.py              # Streamlit UI
```

## License

MIT © 2026 Doston Sultonov.
