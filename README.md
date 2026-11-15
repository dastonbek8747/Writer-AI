# ✍️ Writer AI — AI Yozuvchi

**FastAPI** backend + **Streamlit** frontend asosidagi AI matn yozish yordamchisi. Foydalanuvchi so'rovi bo'yicha matn yaratadi va DOCX faylga yozadi.

---

## ✨ Imkoniyatlar

- ✍️ **AI matn yozish:** mavzu bo'yicha matn yaratish
- 📄 **DOCX eksport:** tayyor matnni Word faylga saqlash
- 🔐 **Foydalanuvchilar:** ro'yxatdan o'tish va parol hashlash
- 🎬 **Streaming javob:** matn bo'lib-bo'lib ko'rsatiladi
- 💾 **Ma'lumotlar bazasi**

---

## 🛠 Texnologiyalar

| Texnologiya | Maqsad |
|---|---|
| **Python 3.12+** | Asosiy til |
| **FastAPI** | Backend |
| **Streamlit** | Frontend |
| **LangChain** | AI |
| **python-docx** | DOCX yozish |
| **uv** | Paket menejeri |

---

## ⚙️ O'rnatish

```bash
git clone https://github.com/dastonbek8747/Writer-AI.git
cd Writer-AI
uv sync
```

`.env` fayl yarating:

```env
GROQ_API_KEY=...
DATABASE_URL=...
```

> 🔒 `.env` git'ga qo'shilmaydi.

---

## ▶️ Ishga tushirish

**Backend:**

```bash
cd backend && uvicorn main:app --reload
```

**Frontend:**

```bash
streamlit run app.py
```

---

## 📁 Loyiha tuzilishi

```
Writer-AI/
├── app.py               # Streamlit frontend
├── api_get_data.py      # Streaming yordamchi
├── backend/
│   ├── main.py          # FastAPI app
│   ├── ai_evalutor.py   # AI mantiqi
│   ├── docx_writer.py   # DOCX eksport
│   ├── db.py            # Ma'lumotlar bazasi
│   ├── users.py         # Foydalanuvchilar
│   └── hashing.py       # Parol hashlash
├── pyproject.toml
└── uv.lock
```

---

## 📄 Litsenziya

Litsenziya ko'rsatilmagan.
