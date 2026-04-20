--- START OF FILE app (1).py ---

import streamlit as st
import google.generativeai as genai
import json
import datetime
from datetime import date, timedelta

# ─── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="FlowMind – AI Trợ Lý Học Sinh",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

/* Dark background */
.stApp { background: #0d0f14; color: #eef0f6; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #13161e !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] * { color: #eef0f6 !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c6ff7, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Be Vietnam Pro', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }

/* Text inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #1a1e2a !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #eef0f6 !important;
    font-family: 'Be Vietnam Pro', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c6ff7 !important;
    box-shadow: 0 0 0 2px rgba(124,111,247,0.2) !important;
}

/* Cards */
.fm-card {
    background: #1e2333;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.fm-stat {
    background: #1e2333;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
}
.fm-stat-val { font-size: 36px; font-weight: 700; margin-bottom: 4px; }
.fm-stat-label { font-size: 13px; color: #8b90a8; }

/* XP bar */
.xp-wrap {
    background: #1a1e2a;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    margin: 8px 0;
}
.xp-fill {
    height: 100%;
    background: linear-gradient(90deg, #7c6ff7, #4ecdc4);
    border-radius: 999px;
    transition: width 0.5s ease;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
}
.badge-purple { background: rgba(124,111,247,0.15); color: #9d99ff; }
.badge-mint   { background: rgba(78,205,196,0.15);  color: #6ee8df; }
.badge-green  { background: rgba(105,219,124,0.15); color: #69db7c; }
.badge-amber  { background: rgba(255,179,71,0.15);  color: #ffb347; }

/* Method cards */
.method-card {
    background: #1a1e2a;
    border-left: 3px solid #7c6ff7;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
}
.method-title { color: #9d99ff; font-weight: 700; font-size: 15px; margin-bottom: 6px; }

/* Chat messages */
.chat-user {
    background: linear-gradient(135deg, #7c6ff7, #6366f1);
    color: white;
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    margin-left: 20%;
    font-size: 14px;
    line-height: 1.6;
}
.chat-ai {
    background: #1e2333;
    color: #eef0f6;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    margin-right: 20%;
    font-size: 14px;
    line-height: 1.6;
}

/* Day schedule */
.day-card {
    background: #1a1e2a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.day-name { color: #9d99ff; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }

/* Leaderboard */
.lb-row {
    display: flex;
    align-items: center;
    gap: 14px;
    background: #1a1e2a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 8px;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ──────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "dashboard",
        "name": "",
        "onboarded": False,
        "focus_duration": "30 phút",
        "learning_style": "Hình ảnh",
        "stress": 3,
        "xp": 0,
        "streak": 1,
        "tasks_done": 0,
        "chat_history": [],
        "api_key": "",
        "gemini_configured": False,
        "last_login": str(date.today()),
        "schedule_result": "",
        "method_result": "",
        "quiz_questions": [],
        "quiz_index": 0,
        "quiz_score": 0,
        "quiz_done": False,
        "quiz_answered": False,
        "quiz_selected": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── GEMINI CONFIG ──────────────────────────────────────────────
def configure_gemini(key):
    try:
        genai.configure(api_key=key)
        st.session_state.gemini_configured = True
        st.session_state.api_key = key
        return True
    except Exception as e:
        print(f"Error configuring Gemini: {e}")  # Print the error for debugging
        return False

def call_ai(prompt, system_prompt="", max_tokens=1500):
    if not st.session_state.gemini_configured:
        return "⚠️ Chưa có API key. Vui lòng nhập Gemini API key ở sidebar."
    try:
        model = genai.GenerativeModel(
            model_name="gemini-pro",  # Use a valid model name
            system_instruction=system_prompt if system_prompt else None
        )
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=max_tokens
            )
        )
        return response.text
    except Exception as e:
        return f"⚠️ Lỗi: {str(e)}"

# ─── HELPERS ───────────────────────────────────────────────────
def add_xp(amount):
    st.session_state.xp += amount
    st.toast(f"🎉 +{amount} XP!", icon="⭐")

def get_level():
    xp = st.session_state.xp
    if xp >= 300: return "🏆 Thủ khoa", 300, 500
    if xp >= 100: return "⭐ Học sinh giỏi", 100, 300
    return "🎓 Học sinh", 0, 100

def xp_bar_html(xp, min_xp, max_xp):
    pct = min(100, int((xp - min_xp) / (max_xp - min_xp) * 100)) if max_xp > min_xp else 0
    return f"""
    <div class="xp-wrap">
      <div class="xp-fill" style="width:{pct}%"></div>
    </div>
    """

# ─── ONBOARDING ────────────────────────────────────────────────
if not st.session_state.onboarded:
    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px;">
      <div style="font-size:48px;margin-bottom:12px;">🧠</div>
      <h1 style="font-size:32px;font-weight:700;background:linear-gradient(90deg,#9d99ff,#6ee8df);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">
        FlowMind
      </h1>
      <p style="color:#8b90a8;font-size:16px;">AI Trợ Lý Học Sinh — Người bạn đồng hành của bạn</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 👋 Xin chào! Mình là FlowMind")
        name = st.text_input("Tên của bạn là gì?", placeholder="Nhập tên...")

        st.markdown("**Bạn thường tập trung được bao lâu?**")
        focus = st.select_slider("", options=["15 phút", "30 phút", "45 phút", "1 tiếng+"], value="30 phút", label_visibility="collapsed")

        st.markdown("**Phong cách học của bạn?**")
        style = st.selectbox("", ["👁️ Hình ảnh", "👂 Nghe", "📝 Đọc/Viết", "🤝 Thực hành"], label_visibility="collapsed")

        st.markdown("**Mức độ áp lực hiện tại (1=thoải mái, 5=rất căng)**")
        stress = st.slider("", 1, 5, 3, label_visibility="collapsed")

        if st.button("🚀 Bắt đầu với FlowMind!", use_container_width=True):
            if name.strip():
                st.session_state.name = name.strip()
                st.session_state.focus_duration = focus
                st.session_state.learning_style = style.split(" ", 1)[1] if " " in style else style
                st.session_state.stress = stress
                st.session_state.onboarded = True
                st.session_state.xp = 5
                st.rerun()
            else:
                st.error("Vui lòng nhập tên của bạn!")
    st.stop()

# ─── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:24px;padding:0 4px;">
      <div style="width:36px;height:36px;background:linear-gradient(135deg,#7c6ff7,#4ecdc4);
           border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;">🧠</div>
      <span style="font-size:20px;font-weight:700;background:linear-gradient(90deg,#9d99ff,#6ee8df);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;">FlowMind</span>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "dashboard":   ("🏠", "Tổng quan"),
        "schedule":    ("📅", "Lịch trình"),
        "method":      ("📚", "Phương pháp"),
        "quiz":        ("✍️", "Bài kiểm tra"),
        "chat":        ("💬", "Tâm sự"),
        "leaderboard": ("🏆", "Bảng xếp hạng"),
    }
    for key, (icon, label) in pages.items():
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.divider()
    st.markdown("**⚙️ Gemini API Key**")
    api_input = st.text_input("", type="password", placeholder="AIzaSy...", label_visibility="collapsed", value=st.session_state.api_key)
    if st.button("Lưu & kết nối", use_container_width=True):
        if configure_gemini(api_input):
            st.success("✅ Kết nối thành công!")
        else:
            st.error("Key không đúng!")
    st.caption("Lấy free tại aistudio.google.com")

    if st.session_state.gemini_configured:
        st.markdown('<div