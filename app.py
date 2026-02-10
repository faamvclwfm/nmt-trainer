import streamlit as st
import json
import random

st.set_page_config(page_title="NMT Multi-Trainer", layout="wide")

def load_data():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

def reset_state():
    st.session_state.current_q = None
    st.session_state.answered = False
    st.session_state.score = 0
    st.session_state.total = 0

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Англійська: Загальні тести"
    reset_state()

st.sidebar.header("🎓 Оберіть предмет")
mode = st.sidebar.selectbox(
    "Режим тренування:", 
    [
        "Англійська: Загальні тести", 
        "Англійська: Confusing Words", 
        "Історія: Цитати НМТ",
        "Українська: Тренажер наголосів"
    ]
)

if st.session_state.current_mode != mode:
    st.session_state.current_mode = mode
    reset_state()
    st.rerun()

# Логіка фільтрації
if mode == "Англійська: Confusing Words":
    questions = [q for q in data if "Confusing" in str(q.get('type', ''))]
    title = "🎯 Confusing Words Trainer"
elif mode == "Історія: Цитати НМТ":
    questions = [q for q in data if "History" in str(q.get('type', ''))]
    title = "📜 Тренажер історичних цитат"
elif mode == "Українська: Тренажер наголосів":
    questions = [q for q in data if "Accent" in str(q.get('type', ''))]
    title = "🗣️ Наголоси у словах (Укр. мова)"
else:
    questions = [q for q in data if all(k not in str(q.get('type', '')) for k in ["Confusing", "History", "Accent"])]
    title = "📚 Англійська мова: Основна підготовка"

st.title("🚀 NMT Ultimate Trainer")
st.subheader(title)

if not questions:
    st.error(f"У файлі questions.json не знайдено питань для режиму: {mode}")
    st.stop()

if st.session_state.current_q is None or st.session_state.current_q not in questions:
    st.session_state.current_q = random.choice(questions)
    st.session_state.answered = False

q = st.session_state.current_q

# Відображення питання
st.info(f"**Завдання:** {q['text']}")
if q.get('question'):
    st.warning(f"❓ {q['question']}")

options = q['options']
cols = st.columns(len(options))

for i, key in enumerate(options):
    label = options[key] if isinstance(options, dict) else key
    if cols[i].button(label, disabled=st.session_state.answered, key=f"btn_{mode}_{i}"):
        st.session_state.answered = True
        st.session_state.total += 1
        if key == q['correct_answer']:
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

# Статистика в сайдбарі
st.sidebar.divider()
st.sidebar.write(f"📊 **Рахунок:** {st.session_state.score} / {st.session_state.total}")
st.sidebar.write(f"📂 Доступно питань: {len(questions)}")
if st.sidebar.button("Скинути прогрес"):
    reset_state()
    st.rerun()