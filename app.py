import streamlit as st
import json
import random


def load_data():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

st.title("🚀 NMT English Ultimate Trainer")


st.sidebar.header("Налаштування")
mode = st.sidebar.selectbox(
    "Оберіть режим:", 
    ["Загальний тест (500 питань)", "Тренажер Confusing Words"]
)


if mode == "Тренажер Confusing Words":
    questions = [q for q in data if q.get('type') == 'Confusing Words']
    st.subheader("🎯 Тренуємо слова, які часто плутають")
else:
    questions = [q for q in data if q.get('type') != 'Confusing Words']
    st.subheader("📚 Підготовка до основних завдань НМТ")


if 'current_q' not in st.session_state:
    st.session_state.current_q = random.choice(questions)
    st.session_state.score = 0
    st.session_state.total = 0

q = st.session_state.current_q

st.info(f"Питання: {q['text']}")

cols = st.columns(len(q['options']))
for i, option in enumerate(q['options']):
    if cols[i].button(option):
        st.session_state.total += 1
        if option == q['correct_answer']:
            st.success("✅ Правильно!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Помилка! Правильна відповідь: {q['correct_answer']}")
        
        st.write(f"💡 **Пояснення:** {q['explanation']}")
        
        if st.button("Наступне питання ➡️"):
            st.session_state.current_q = random.choice(questions)
            st.rerun()

st.sidebar.divider()
st.sidebar.write(f"📊 Рахунок: {st.session_state.score} / {st.session_state.total}")