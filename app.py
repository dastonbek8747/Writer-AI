import time
import streamlit as st
from api_get_data import write_stream_streamlit
import requests as rq

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Synora AI", page_icon="✍️", layout="wide")

if "session_id" not in st.session_state:
    st.session_state["session_id"] = ""
if "aproved" not in st.session_state:
    st.session_state["aproved"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}

.synora-hero {
    text-align: center;
    padding: 40px 0 10px 0;
}
.synora-hero h1 {
    font-size: 46px;
    font-weight: 800;
    background: linear-gradient(90deg, #a18cd1, #fbc2eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}
.synora-hero p {
    color: #c9c3e0;
    font-size: 16px;
    margin-top: 4px;
}

.auth-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 30px 35px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.stTextInput input, .stTextInput input:focus {
    background-color: rgba(255,255,255,0.07);
    color: white;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.15);
}

.stButton button {
    background: linear-gradient(90deg, #a18cd1, #fbc2eb);
    color: #1c1c2b;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 8px 20px;
    transition: 0.2s;
}
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(161, 140, 209, 0.4);
}

.topic-card {
    background: rgba(255, 255, 255, 0.06);
    border-left: 4px solid #a18cd1;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
}
.topic-card h4 {
    color: #fbc2eb;
    margin-bottom: 4px;
}
.topic-card p {
    color: #e3e0f0;
    font-size: 14px;
    line-height: 1.6;
}

.reja-item {
    background: rgba(161, 140, 209, 0.12);
    border-radius: 8px;
    padding: 8px 14px;
    margin-bottom: 6px;
    color: #e8e5f5;
    font-size: 14px;
}

.info-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 22px;
}
.info-card h3 {
    color: #fbc2eb;
    font-size: 19px;
    margin-bottom: 10px;
}
.info-card p {
    color: #dcd8ee;
    font-size: 14.5px;
    line-height: 1.7;
    margin-bottom: 10px;
}
.info-card .misol {
    background: rgba(161, 140, 209, 0.12);
    border-radius: 8px;
    padding: 6px 12px;
    margin-bottom: 6px;
    color: #e8e5f5;
    font-size: 13.5px;
    display: inline-block;
    margin-right: 8px;
}

button[kind="secondary"] {
    background: transparent !important;
    color: #dcd8ee !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    font-weight: 500 !important;
}
button[kind="secondary"]:hover {
    background: rgba(255, 90, 90, 0.12) !important;
    border: 1px solid rgba(255, 90, 90, 0.5) !important;
    color: #ff8a8a !important;
    transform: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

if not st.session_state.aproved:
    st.markdown("""
    <div class="synora-hero">
        <h1>Synora AI</h1>
        <p>Kurs ishi va mustaqil ishlaringizni AI yordamida professional darajada tayyorlang</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🆕 Ro'yhatdan o'tish", "🔑 Kirish"])

        with tab1:
            email = st.text_input("Email", key="royhatdan_otish_email")
            password = st.text_input("Parol", type="password", key="royhat_otish_password")
            confirm_password = st.text_input("Parolni tasdiqlang", type="password", key="royhat_otish_confirm_password")
            submit_button = st.button("Ro'yhatdan o'tish", use_container_width=True)

            if submit_button:
                if password != confirm_password:
                    st.warning("Parollar mos kelmadi")
                else:
                    response = rq.post(f"{API_URL}/register",
                                        json={"email": email, "password": password,
                                              "confirm_password": confirm_password})
                    if response.json()['message'] == "User created successfully":
                        st.session_state.session_id = response.json()['new_user']["session_id"]
                        st.session_state.aproved = True
                        st.balloons()
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(response.json()['message'])

        with tab2:
            email = st.text_input("Email", key="kirish_email")
            password = st.text_input("Parol", type="password", key="kirish_password")
            btn = st.button("Kirish", use_container_width=True)

            if btn:
                response = rq.post(f"{API_URL}/login", json={"email": email, "password": password})
                if response.json()["message"] == "Login successful":
                    st.session_state.session_id = response.json()['user']["session_id"]
                    st.session_state.aproved = True
                    st.balloons()
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error(response.json()['message'])

        st.markdown('</div>', unsafe_allow_html=True)

else:
    top_col1, top_col2 = st.columns([6, 1])
    with top_col1:
        st.markdown("""
        <div class="synora-hero" style="text-align: left; padding: 10px 0 0 0;">
            <h1 style="font-size: 30px;">Synora AI</h1>
        </div>
        """, unsafe_allow_html=True)
    with top_col2:
        st.write("")
        if st.button("🚪 Chiqish", use_container_width=True, type="secondary"):
            st.session_state.aproved = False
            st.session_state.session_id = ""
            st.rerun()

    st.markdown("""
    <div class="info-card">
        <h3>Xush kelibsiz 👋</h3>
        <p>Bu yerda siz kurs ishi yoki mustaqil ish uchun mavzu yozasiz, men esa shu mavzuni
        bo'limlarga ajratib, har biri bo'yicha chuqur va professional matn yozib, tayyor
        Word (.docx) faylini taqdim etaman.</p>
        <p>Pastdagi maydonga mavzuingizni yozing, masalan:</p>
        <span class="misol">Alisher Navoiy ijodida inson konsepsiyasi</span>
        <span class="misol">O'zbek tilida frazeologizmlarning uslubiy xususiyatlari</span>
        <span class="misol">Sog'lom turmush tarzi va uning ahamiyati</span>
    </div>
    """, unsafe_allow_html=True)

    user_request = st.chat_input("Mavzuni shu yerga yozing...")

    if user_request:
        with st.chat_message("user"):
            st.write(user_request)

        with st.status("Mavzu o'rganib chiqilmoqda...", expanded=True) as status:
            st.write("📋 Rejalar tuzilmoqda...")
            response_ai = rq.post(f"{API_URL}/writer_ai",
                                   json={'message': user_request, "session_id": st.session_state.session_id})
            st.write("📚 Rejalar asosida ma'lumotlar to'planmoqda...")
            status.update(label="Tayyor ✔  Word faylga ko'chirilmoqda...", expanded=False, state="complete")

        data = response_ai.json()
        mavzusi = data['topic']
        rejalar = data['tasks']
        results = data['results']
        file_name = data.get('file_name')

        with st.sidebar:
            st.markdown(f"""
            <div class="topic-card">
                <h4>📌 Mavzu</h4>
                <p>{mavzusi}</p>
            </div>
            """, unsafe_allow_html=True)


            if file_name:
                file_response = rq.get(f"{API_URL}/download_docx/{file_name}")
                st.download_button(
                    label="📄 Word faylni yuklab olish",
                    data=file_response.content,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

        st.markdown("### 📖 Natijalar")
        for i in range(len(rejalar)):
            with st.expander(f"{i + 1}. {rejalar[i]}", expanded=(i == 0)):
                st.write_stream(write_stream_streamlit(results[i]))