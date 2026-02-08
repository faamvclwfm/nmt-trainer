import streamlit as st
import json
import random


st.set_page_config(page_title="НМТ Англійська: Тренажер", page_icon="🇬🇧")


@st.cache_data
def load_questions():
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Помилка завантаження бази питань: {e}")
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
        new_q = random.choice(questions)
        if len(questions) > 1:
            while new_q['id'] == st.session_state.current_question['id']:
                new_q = random.choice(questions)
        st.session_state.current_question = new_q
    st.session_state.answered = False

st.title("🇬🇧 NMT English Practice")
st.sidebar.metric("Результат", f"{st.session_state.score}/{st.session_state.total}")

if st.session_state.current_question:
    q = st.session_state.current_question
    st.caption(f"📌 {q.get('type')} | Рік: {q.get('year')}")
    
    if q.get('text'):
        st.markdown(f"**Read the text:**\n{q['text']}")
    
    st.subheader(q.get('question'))
    
    options = q.get('options', {})
    user_choice = st.radio(
        "Варіанти:", 
        list(options.keys()), 
        format_func=lambda x: f"{x}) {options[x]}",
        key=f"radio_{q.get('id')}",
        disabled=st.session_state.answered
    )

    if not st.session_state.answered:
        if st.button("Перевірити ✅", use_container_width=True):
            st.session_state.answered = True
            st.session_state.total += 1
            if user_choice == q['correct_answer']:
                st.success("Правильно!")
                st.session_state.score += 1
            else:
                st.error(f"Неправильно. Правильна відповідь: {q['correct_answer']}")
    

    if st.session_state.answered:
        st.info(f"💡 **Пояснення:**\n\n{q.get('explanation', 'Пояснення скоро буде додано.')}")
        st.button("Наступне питання ➡️", on_click=next_question, use_container_width=True)

else:
    st.warning("Питання не знайдені.")