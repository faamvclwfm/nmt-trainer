import streamlit as st
import json
import random
import google.generativeai as genai
import os


st.set_page_config(page_title="НМТ Англійська + AI", page_icon="🇬🇧")


@st.cache_data
def load_questions():
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Помилка завантаження JSON: {e}")
        return []

questions = load_questions()


if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'current_question' not in st.session_state:
    if questions:
        st.session_state.current_question = random.choice(questions)
    else:
        st.session_state.current_question = None


def next_question():
    if questions:
        st.session_state.current_question = random.choice(questions)
    st.session_state.answered = False



st.title("🇬🇧 НМТ English Trainer")
st.sidebar.metric("Мій результат", f"{st.session_state.score}/{st.session_state.total}")

if st.session_state.current_question:
    q = st.session_state.current_question
    
    st.info(f"Завдання: {q['type']} ({q['year']} рік)")
    if q.get('text'):
        st.markdown(f"**Read the text:**\n{q['text']}")
    
    st.subheader(q['question'])
    
    options = list(q['options'].keys())
    user_choice = st.radio(
        "Обери відповідь:", 
        options, 
        format_func=lambda x: f"{x}) {q['options'][x]}",
        key=f"q_{q['id']}"
    )

    if st.button("Перевірити"):
        st.session_state.answered = True
        st.session_state.total += 1
        
        if user_choice == q['correct_answer']:
            st.success("✅ Правильно!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Неправильно. Правильна відповідь: {q['correct_answer']}")

        if "GOOGLE_API_KEY" in st.secrets:
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner('🤖 ШІ-тьютор готує пояснення...'):
                    prompt = f"""
                    Ти вчитель англійської мови. Поясни коротким текстом українською мовою, 
                    чому в цьому питанні правильна відповідь {q['correct_answer']}.
                    Контекст: {q.get('text', '')}
                    Питання: {q['question']}
                    Варіант учня: {user_choice}
                    """
                    response = model.generate_content(prompt)
                    st.info(f"🤖 Пояснення ШІ:\n\n{response.text}")
            except Exception as e:
                st.warning(f"ШІ тимчасово недоступний: {e}")
        else:
            st.warning("API ключ не знайдено в Secrets.")


    if st.session_state.answered:
        st.button("Наступне питання ➡️", on_click=next_question)
else:
    st.write("Питання не знайдені. Перевір файл questions.json")