# app.py
import streamlit as st
import os
import openai
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # غيّر للموديل الذي تستخدمه

openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="ChatAr — شات عربي", layout="wide")
st.title("🤖 ChatAr — شات ذكاء صناعي بالعربية")
st.markdown("واجهة بسيطة للدردشة بالعربية. أدخل سؤالك واضغط **إرسال**.")

# الجلسة: تاريخ المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "أنت مساعد ذكي يتحدث العربية بطلاقة، مختصر ومفيد."}
    ]

# شريط إعدادات جانبي
with st.sidebar:
    st.header("الإعدادات")
    model = st.text_input("اسم الموديل (Model)", value=MODEL)
    max_tokens = st.slider("الحد الأقصى للـ tokens", 50, 2000, 800)
    temperature = st.slider("الحرارة (creativity)", 0.0, 1.0, 0.2)
    if st.button("مسح المحادثة"):
        st.session_state.messages = [
            {"role": "system", "content": "أنت مساعد ذكي يتحدث العربية بطلاقة، مختصر ومفيد."}
        ]
        st.success("تم مسح تاريخ المحادثة.")

# إدخال المستخدم
user_input = st.text_input("اكتب سؤالك هنا...", key="input")
col1, col2 = st.columns([1, 4])
with col1:
    send = st.button("إرسال")

# عرض المحادثة
def render_messages():
    for m in st.session_state.get("messages", [])[1:]:
        role = m["role"]
        content = m["content"]
        if role == "user":
            st.markdown(f"**أنت:** {content}")
        else:
            st.markdown(f"**ChatAr:** {content}")

st.markdown("---")
render_messages()

# دالة للنداء إلى API مع إعادة المحاولة
@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
def call_openai(messages, model_name, temp, max_tokens):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        temperature=temp,
        max_tokens=max_tokens,
        n=1,
    )
    return response

if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    with st.spinner("جاري الحصول على الإجابة..."):
        try:
            resp = call_openai(st.session_state.messages, model, temperature, max_tokens)
            # دعم لهياكل استجابة مختلفة — استخرج النص بأمان
            if "choices" in resp and len(resp.choices) > 0:
                assistant_msg = resp.choices[0].message.get("content", "").strip()
            else:
                assistant_msg = str(resp)
            st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بمزود الخدمة: {e}")
    # إعادة عرض
    st.experimental_rerun()
