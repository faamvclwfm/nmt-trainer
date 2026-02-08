import streamlit as st
import json
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NMT English Ultimate Trainer", layout="wide")

@st.cache_data
def load_data():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

def reset_state():
    st.session_state.current_q = None
    st.session_state.answered = False
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.history = []

if "history" not in st.session_state:
    st.session_state.history = []

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Загальний тест (500 питань)"
    reset_state()

st.sidebar.header("Налаштування")
mode = st.sidebar.selectbox(
    "Оберіть режим:", 
    ["Загальний тест (500 питань)", "Тренажер Confusing Words"]
)

if st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    reset_state()
    st.rerun()

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

st.info(f"**Контекст:** {q['text']}")
if 'question' in q and q['question']:
    st.warning(f"❓ **Запитання:** {q['question']}")

options = q['options']
cols = st.columns(len(options))

for i, key in enumerate(options):
    label = options[key] if isinstance(options, dict) else key
    if cols[i].button(label, disabled=st.session_state.answered, key=f"btn_{i}"):
        st.session_state.answered = True
        st.session_state.total += 1
        is_correct = key == q['correct_answer']
        
        st.session_state.history.append({
            "Час": datetime.now().strftime("%H:%M:%S"),
            "Питання": q['text'][:50] + "...",
            "Ваша відповідь": label,
            "Результат": "✅" if is_correct else "❌"
        })

        if is_correct:
            st.success("✅ Правильно!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Помилка! Правильна відповідь: {q['correct_answer']}")
        st.write(f"💡 **Пояснення:** {q.get('explanation', '')}")

if st.session_state.answered:
    if st.button("Наступне питання ➡️"):
        st.session_state.current_q = random.choice(questions)
        st.session_state.answered = False
        st.rerun()

st.sidebar.divider()
st.sidebar.write(f"📊 **Рахунок:** {st.session_state.score} / {st.session_state.total}")

if st.session_state.history:
    st.sidebar.subheader("Збереження")
    df = pd.DataFrame(st.session_state.history)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.sidebar.download_button(
        label="📥 Завантажити результати (CSV)",
        data=csv,
        file_name=f"nmt_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )

if st.sidebar.button("Скинути прогрес"):
    reset_state()
    st.rerun()