import streamlit as st
import json
import random
import google.generativeai as genai
import os


st.set_page_config(page_title="НМТ Англійська + AI", page_icon="🇬🇧")

st.title("🇬🇧 НМТ English Trainer + AI Tutor")
st.write("Тренуйся на реальних тестах, а ШІ пояснить помилки!")


@st.cache_data
def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

questions = load_questions()


if 'current_question' not in st.session_state:
    st.session_state.current_question = random.choice(questions)
    st.session_state.answered = False

def next_question():
    st.session_state.current_question = random.choice(questions)
    st.session_state.answered = False


q = st.session_state.current_question

st.info(f"**Тип завдання:** {q['type']}")
if q.get('text'):
    st.text_area("Read the text:", value=q['text'], height=150, disabled=True)

st.subheader(q['question'])


options = list(q['options'].keys())
choice = st.radio("Обери варіант:", options, format_func=lambda x: f"{x}) {q['options'][x]}")


if st.button("Перевірити відповідь") and not st.session_state.answered:
    st.session_state.answered = True
    
    user_choice = choice
    correct_choice = q['correct_answer']
    
    if user_choice == correct_choice:
        st.success(f"✅ Правильно! Це дійсно варіант {correct_choice}.")
    else:
        st.error(f"❌ Неправильно. Ти обрав {user_choice}, а правильно {correct_choice}.")


    if "GOOGLE_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('🤖 ШІ-тьютор аналізує твою відповідь...'):
                prompt = f"""
                Ти досвідчений вчитель англійської (НМТ).
                Текст: "{q.get('text', '')}"
                Питання: "{q['question']}"
                Варіант студента: "{user_choice}"
                Правильний варіант: "{correct_choice}"
                
                Поясни українською мовою, чому ця відповідь правильна.
                """
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("### 🤖 Коментар ШІ-тьютора:")
                    st.info(response.text)
                    
        except Exception as e:
            st.error(f"⚠️ Помилка ШІ: {e}")
    else:
        st.warning("⚠️ Не знайдено API ключ у Secrets.")

if st.session_state.answered:
    st.button("Наступне питання ➡️", on_click=next_question)