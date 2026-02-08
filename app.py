import streamlit as st
import json
import random


st.set_page_config(page_title="NMT English Ultimate Trainer", layout="wide")


@st.cache_data
def load_data():
   
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()


def reset_state():
    st.session_state.current_q = None
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.answered = False


st.sidebar.header("Налаштування")
mode = st.sidebar.selectbox(
    "Оберіть режим:", 
    ["Загальний тест (500 питань)", "Тренажер Confusing Words"],
    on_change=reset_state 
)

if "current_mode" not in st.session_state or st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    reset_state()


if mode == "Тренажер Confusing Words":
    questions = [q for q in data if q.get('type') == 'Confusing Words']
    title = "🎯 Тренуємо слова, які часто плутають"
else:
    questions = [q for q in data if q.get('type') != 'Confusing Words']
    title = "📚 Підготовка до основних завдань НМТ"

st.title("🚀 NMT English Ultimate Trainer")
st.subheader(title)


if st.session_state.current_q is None:
    st.session_state.current_q = random.choice(questions)
    st.session_state.answered = False

q = st.session_state.current_q


st.info(f"**Питання:** {q['text']}")


options_list = list(q['options'].values()) if isinstance(q['options'], dict) else q['options']
cols = st.columns(len(options_list))

for i, option_text in enumerate(options_list):
    option_key = list(q['options'].keys())[i] if isinstance(q['options'], dict) else option_text
    
    if cols[i].button(f"{option_key}: {option_text}", disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        
        if option_key == q['correct_answer']:
            st.success("✅ Правильно!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Помилка! Правильна відповідь: {q['correct_answer']}")
        
        st.write(f"💡 **Пояснення:** {q.get('explanation', 'Пояснення відсутнє')}")


if st.session_state.answered:
    if st.button("Наступне питання ➡️"):
        st.session_state.current_q = random.choice(questions)
        st.session_state.answered = False
        st.rerun()


st.sidebar.divider()
st.sidebar.write(f"📊 **Рахунок:** {st.session_state.score} / {st.session_state.total}")
if st.sidebar.button("Скинути прогрес"):
    reset_state()
    st.rerun()