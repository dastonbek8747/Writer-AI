from langgraph.graph import START, StateGraph, END
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal, List
from dotenv import load_dotenv
from langchain_postgres import PostgresChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
import psycopg
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor
import os
import streamlit as st

load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY_2")
API_KEY = st.secrets["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", api_key=API_KEY)
parser = StrOutputParser()
con = psycopg.connect(os.getenv("DATABASE_URL"))
PostgresChatMessageHistory.create_tables(con, "chat_history")


class llm_schema(BaseModel):
    tasks: List[str]


llm_with_schema = llm.with_structured_output(llm_schema)


class graph_schema(TypedDict):
    topic: str
    tasks: List[str]
    results: List[str]


def generate_tasks(state: graph_schema) -> graph_schema:
    topic = state["topic"]
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system",
    #      "Siz aqlli dastur yordamchisiz ! Sizga mavzu beriladi siz shu mavzuni murakkab rejalarga ajratib olishingiz kerak bo'ladi."),
    #     ('human', "MAVZU : {topic}. Rejalar mavzudan chetlashmagan holda va mavzuni to'liq qamrab olishi shart !")
    # ])
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Siz o'zbek tili va adabiyoti bo'yicha ko'p yillik tajribaga ega, yuqori "
         "malakali metodist-o'qituvchisiz. Sizga berilgan mavzu (mumtoz yoki zamonaviy "
         "adabiyot, tilshunoslik, adabiy janr, ijodkor hayoti va ijodi, badiiy asar tahlili "
         "va h.k.) bo'yicha o'quvchilar/talabalar uchun chuqur va tizimli o'rganish rejasini "
         "tuzishingiz kerak.\n\n"
         "QOIDALAR:\n"
         "- Kamida 4, ko'pi bilan 10 ta subtopic (mavzu bo'limi) yarating\n"
         "- Har bir subtopic mavzuning butunlay boshqa qirrasini yoritsin. Masalan (mavzu "
         "turiga qarab moslashtiring): tarixiy-adabiy kontekst, ijodkor yoki davr haqida "
         "ma'lumot, asarning g'oyaviy-badiiy tahlili, til va uslub xususiyatlari, janr "
         "xususiyatlari, timsollar va obrazlar tahlili, tarbiyaviy-axloqiy ahamiyati, "
         "boshqa asarlar/ijodkorlar bilan qiyosiy tahlil, zamonaviy adabiyotshunoslikdagi "
         "o'rni, xulosa va amaliy tavsiyalar (masalan insho yozish yoki dars o'tish uchun)\n"
         "- Har bir subtopic o'zi mustaqil ravishda 500-800 so'zlik chuqur, ilmiy-metodik "
         "jihatdan asoslangan javob berishga yetarli darajada keng va boy bo'lsin — juda "
         "tor, umumiy yoki bir jumlali bo'lmasin\n"
         "- Subtopiclar bir-birini takrorlamasin, bir-biriga mazmunan aralashib ketmasin, "
         "har biri aniq va konkret chegaraga ega bo'lsin\n"
         "- Subtopiclar nomi o'quvchiga tushunarli, adabiyotshunoslik va tilshunoslik "
         "terminologiyasiga mos, professional tarzda shakllantirilsin"),
        ('human',
         "MAVZU: {topic}\n\n"
         "Ushbu mavzuni yuqoridagi qoidalarga ko'ra subtopiclarga ajrating. Rejalar "
         "mavzudan chetlashmagan holda mavzuni har tomonlama, chuqur va to'liq qamrab "
         "olishi shart! Har bir subtopic keyinchalik alohida-alohida kengaytirilib, "
         "to'liq maqola sifatida yoziladi, shuni hisobga oling.")
    ])
    chain = prompt | llm_with_schema
    response = chain.invoke({"topic": topic})
    state["tasks"] = response.tasks
    return state


def generate_results(request: str):
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system",
    #      "Siz aqlli dastur yordamchisiz. Sizga berilgan mavzu bo'yicha to'liq qilib batafsil ma'lumot bering !"),
    #     ("human", "{request}")
    # ])
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
Siz o'zbek tili va adabiyoti bo'yicha yuqori toifali, ilmiy-metodik yondashuvga ega
professional o'qituvchi va maqola muallifisiz.

Sizning vazifangiz berilgan mavzu (subtopic) bo'yicha Word (.docx) hujjatiga tayyor
holatda joylashtiriladigan, o'quv-ilmiy uslubdagi to'liq matn yozishdir.

QOIDALAR:

1. Matn 700-900 so'zdan kam bo'lmasin. Mavzu keng bo'lsa, hajmni qisqartirmang —
   aksincha, har bir jihatni misollar va tahlillar bilan to'liq yoriting.

2. Matn quyidagi tartibda yozilsin:

Kirish

1. ...
2. ...
3. ...
4. ...
5. ...

Muammolar va xavflar

Xulosa

Tavsiyalar

3. Har bir bo'lim batafsil, chuqur va izchil tushuntirilsin. Yuzaki yoki umumiy
   ta'riflar bilan cheklanmang.

4. Har bir fikr imkon qadar aniq misollar bilan asoslansin: adabiy asarlardan
   parchalar mazmuni, ijodkorlar hayotidan faktlar, tarixiy-adabiy ma'lumotlar,
   tilshunoslik qoidalariga oid namunalar yoki real o'quv jarayonidagi holatlar
   bilan boyitilsin.

5. Matnda mazmuniy yoki so'z birikmalari darajasidagi takrorlanishlar bo'lmasin.

6. Juda sodda, umumiy yoki "kirish darslik" darajasidagi gaplardan foydalanmang —
   matn adabiyotshunoslik va tilshunoslik nuqtai nazaridan ilmiy jihatdan asoslangan
   bo'lsin.

7. Faqat oddiy matn yozing.

MUHIM:

- Markdown ishlatmang.
- ## ishlatmang.
- ### ishlatmang.
- ** belgilarini ishlatmang.
- * belgilarini ishlatmang.
- > belgilarini ishlatmang.
- ``` belgilarini ishlatmang.
- --- belgilarini ishlatmang.
- Jadval yozmang.
- Emoji ishlatmang.

Faqat Word hujjati uchun toza, formatlanmagan, professional uslubdagi matn yozing.
"""
        ),
        (
            "human",
            """
Mavzu:

{request}

Yuqoridagi qoidalarga to'liq amal qilgan holda, ona tili va adabiyoti fani bo'yicha
professional, chuqur va batafsil maqola yozing. Matnni hech qanday sababga ko'ra
qisqartirmang, mavzuni imkon qadar keng va aniq yoriting.
"""
        )
    ])
    chain = prompt | llm | parser
    return chain.invoke({"request": request})


def executer_node(state: graph_schema) -> graph_schema:
    tasks = state["tasks"]

    with ThreadPoolExecutor(len(tasks)) as executor:
        results = list(executor.map(generate_results, tasks))

    state["results"] = results
    return state


graph = StateGraph(graph_schema)

graph.add_node("generate_tasks", generate_tasks)
graph.add_node("executer_node", executer_node)
graph.add_edge(START, "generate_tasks")
graph.add_edge("generate_tasks", "executer_node")
graph.add_edge("executer_node", END)

compile_graph = graph.compile()


def writer_ai(topic: str) -> graph_schema:
    response = compile_graph.invoke({
        "topic": topic,
        "tasks": [],
        "results": []
    })
    return response


# topic = "Sog'lom turmush tarzi va uning inson salomatligiga ta'siri"


class check_input(BaseModel):
    type_input: Literal["chat", "writer"] = Field(...,
                                                  description="Berilgan matinda nima qilishini aniqlashimiz kerak. Oddiy chat demoqdami yoki biror narsani yozib batafsil tushintirishimizni soramoqdami!")
    topic_output: str


llm_check_input = llm.with_structured_output(check_input)


class gemini_schema(TypedDict):
    topic_input: str
    type_input: str
    session_id: str
    ai_topic: str
    response: str
    result_writer: dict


def save_chat_history(session_id: str):
    chat_history = PostgresChatMessageHistory("chat_history", session_id, sync_connection=con)
    return chat_history


def chat_base(state: gemini_schema) -> gemini_schema:
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Siz aqlli dasturchisiz ! Foydalanuvchi savollariga aniq va to'liq javob bering. Foydalanuvchi bilan hushmuomila munosabatda muloqot olib boring"),
        MessagesPlaceholder(variable_name="chat_history"),
        ('human', "{message}")
    ])
    chain = prompt | llm
    chain_with_history = RunnableWithMessageHistory(
        chain,
        save_chat_history,
        history_messages_key="chat_history",
        input_messages_key="message",
    )
    response = chain_with_history.invoke(
        {"message": state['topic_input']}, config={"configurable": {"session_id": state['session_id']}}
    )
    state['response'] = response.content[0]['text']
    return state


def check_user_input(state: gemini_schema) -> gemini_schema:
    prompt = ChatPromptTemplate.from_template(
        "Siz aqlli dastur yordamchisiz. Sizga foydalanuvchi tomonidan xabar beriladi. XABAR: {message}"
        "Siz ushbu xabarni nima haqiad ekanligini aniqlashingiz kerak bo'ladi. Faqat 100% biror narsani batafsil yoritishini yoki mustaqil yoki kursh ishi yozib ber degan xolatlardagina type_input=writer qilib qaytarib yuborishing shart !")
    chain = prompt | llm_check_input
    response = chain.invoke({"message": state['topic_input']})
    state['type_input'] = response.type_input
    state['ai_topic'] = response.topic_output
    return state


def check_node(state: gemini_schema) -> gemini_schema:
    if state['type_input'] == "chat":
        return "chat"
    else:
        return "writer"


def topic_data_generate(state: gemini_schema):
    yakuniy_natija = compile_graph.invoke({
        "topic": state['ai_topic'],
        "tasks": [],
        "results": []
    })
    state['result_writer'] = yakuniy_natija
    return state


gemini_graph = StateGraph(gemini_schema)

gemini_graph.add_node("check_user_input", check_user_input)
gemini_graph.add_node("chat_base", chat_base)
gemini_graph.add_node("writer", topic_data_generate)

gemini_graph.add_edge(START, "check_user_input")
gemini_graph.add_conditional_edges("check_user_input", check_node, {
    "chat": "chat_base",
    "writer": "writer"
})
gemini_graph.add_edge("writer", END)
gemini_graph.add_edge("chat_base", END)

gemini = gemini_graph.compile()


def gemini_chat(message: str, session_id: str) -> gemini_schema:
    response = gemini.invoke({
        "topic_input": message,
        "type_input": "",
        "session_id": session_id,
        "response": "",
        "ai_topic": "",
        "result_writer": {}
    })
    return response
