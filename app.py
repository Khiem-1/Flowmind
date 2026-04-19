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
    except:
        return False

def call_ai(prompt, system_prompt="", max_tokens=1500):
    if not st.session_state.gemini_configured:
        return "⚠️ Chưa có API key. Vui lòng nhập Gemini API key ở sidebar."
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
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
        st.markdown('<div style="display:flex;align-items:center;gap:6px;margin-top:4px;"><div style="width:8px;height:8px;background:#69db7c;border-radius:50%;"></div><span style="font-size:12px;color:#69db7c;">AI đã kết nối</span></div>', unsafe_allow_html=True)

# ─── DASHBOARD ─────────────────────────────────────────────────
if st.session_state.page == "dashboard":
    hour = datetime.datetime.now().hour
    greet = "Chào buổi sáng" if hour < 12 else "Chào buổi chiều" if hour < 18 else "Chào buổi tối"
    st.markdown(f"## {greet}, {st.session_state.name}! 👋")

    stress_msgs = {1:"Bạn đang rất thoải mái hôm nay! 😌", 2:"Bạn đang khá ổn! 🙂",
                   3:"Hôm nay bình thường, cố lên! 💪", 4:"Bạn đang hơi căng — thở sâu nhé 🌿",
                   5:"Bạn đang rất áp lực — hãy tâm sự với mình nhé 💙"}
    st.caption(stress_msgs.get(st.session_state.stress, ""))

    # XP / Level bar
    level_name, min_xp, max_xp = get_level()
    xp = st.session_state.xp
    st.markdown(f"""
    <div class="fm-card">
      <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
        <span class="badge badge-purple">{level_name}</span>
        <span style="font-size:13px;color:#555a70;">{xp} XP</span>
      </div>
      {xp_bar_html(xp, min_xp, max_xp)}
      <div style="display:flex;justify-content:space-between;font-size:11px;color:#555a70;margin-top:4px;">
        <span>Level hiện tại</span><span>Level tiếp theo ({max_xp} XP)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="fm-stat"><div class="fm-stat-val">🔥 {st.session_state.streak}</div><div class="fm-stat-label">Ngày liên tiếp</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="fm-stat"><div class="fm-stat-val">✅ {st.session_state.tasks_done}</div><div class="fm-stat-label">Nhiệm vụ xong</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="fm-stat"><div class="fm-stat-val">⭐ {st.session_state.xp}</div><div class="fm-stat-label">Tổng XP</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Tính năng")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📅 Quản lý lịch trình\nAI sắp xếp thời khóa biểu tối ưu", use_container_width=True):
            st.session_state.page = "schedule"; st.rerun()
        if st.button("✍️ Tạo bài kiểm tra\nDán tài liệu — AI ra quiz ngay", use_container_width=True):
            st.session_state.page = "quiz"; st.rerun()
    with c2:
        if st.button("📚 Phương pháp học\nPomodoro, Feynman, Shadowing...", use_container_width=True):
            st.session_state.page = "method"; st.rerun()
        if st.button("💬 Tâm sự với AI\nNgười bạn lắng nghe, không phán xét", use_container_width=True):
            st.session_state.page = "chat"; st.rerun()

# ─── SCHEDULE ──────────────────────────────────────────────────
elif st.session_state.page == "schedule":
    st.markdown("## 📅 Quản lý lịch trình")
    st.caption("AI sắp xếp thời gian tối ưu cho bạn")

    with st.form("schedule_form"):
        tkb = st.text_area("📌 Thời khóa biểu cố định",
            placeholder="Thứ 2: Toán 7h-9h, Văn 9h-11h\nThứ 3: Anh 7h-9h, Lý 9h-11h\nThứ 4: Nghỉ\n...",
            height=150)
        tasks = st.text_area("📝 Việc bạn muốn làm thêm",
            placeholder="- Ôn thi Toán (ưu tiên cao)\n- Học tiếng Anh 30 phút/ngày\n- Tập thể dục\n- Hoàn thiện dự án FlowMind",
            height=120)
        submitted = st.form_submit_button("✨ Sắp xếp lịch tối ưu", use_container_width=True)

    if submitted:
        if not tkb and not tasks:
            st.error("Vui lòng nhập thời khóa biểu hoặc việc cần làm!")
        else:
            with st.spinner("AI đang phân tích và sắp xếp lịch..."):
                prompt = f"""Hãy sắp xếp lịch trình tối ưu cho từng ngày trong tuần dựa trên:

Thời khóa biểu cố định:
{tkb or 'Không có'}

Việc cần làm thêm:
{tasks or 'Không có'}

Yêu cầu: ưu tiên công việc quan trọng, có thời gian nghỉ ngơi, không để quá tải. 
Trả lời bằng tiếng Việt, format rõ ràng theo từng ngày trong tuần."""
                result = call_ai(prompt)
                st.session_state.schedule_result = result
                add_xp(5)

    if st.session_state.schedule_result:
        st.markdown("### 📋 Lịch trình gợi ý")
        lines = st.session_state.schedule_result.split('\n')
        current_day = None
        current_tasks = []

        def flush_day(day, tasks_list):
            if not day: return
            tasks_html = ''.join([f'<div style="padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:14px;">• {t}</div>' for t in tasks_list if t.strip()])
            st.markdown(f'<div class="day-card"><div class="day-name">{day}</div>{tasks_html or "<div style=\'color:#555a70;font-size:13px;\'>Nghỉ ngơi 🌿</div>"}</div>', unsafe_allow_html=True)

        for line in lines:
            line = line.strip()
            is_day = any(line.upper().startswith(d) for d in ['THỨ', 'T2','T3','T4','T5','T6','T7','CN','MON','TUE','WED','THU','FRI','SAT','SUN'])
            if is_day:
                flush_day(current_day, current_tasks)
                current_day = line.replace('**','').replace(':','').strip()
                current_tasks = []
            elif current_day and line:
                current_tasks.append(line.lstrip('-•* '))
        flush_day(current_day, current_tasks)

        if not any(any(l.upper().startswith(d) for d in ['THỨ','T2','T3','T4','T5','T6','T7','CN']) for l in lines):
            st.markdown(f'<div class="fm-card" style="white-space:pre-wrap;font-size:14px;line-height:1.8;">{st.session_state.schedule_result}</div>', unsafe_allow_html=True)

        if st.button("✅ Đánh dấu đã xem (+10 XP)"):
            add_xp(10)
            st.session_state.tasks_done += 1
            st.rerun()

# ─── METHOD ────────────────────────────────────────────────────
elif st.session_state.page == "method":
    st.markdown("## 📚 Phương pháp học tập")
    st.caption("AI gợi ý phương pháp phù hợp nhất với bạn")

    with st.form("method_form"):
        subject = st.text_input("📖 Môn học / lĩnh vực muốn cải thiện", placeholder="Toán, Tiếng Anh, Lập trình...")
        problem = st.text_area("😓 Vấn đề bạn gặp khi học",
            placeholder="Hay mất tập trung sau 20 phút, học xong hay quên, không có động lực...",
            height=100)
        style_opts = ["👁️ Hình ảnh / sơ đồ", "👂 Nghe / âm thanh", "📝 Đọc và ghi chú", "🤝 Thực hành / làm"]
        style = st.selectbox("🎯 Phong cách học của bạn", style_opts)
        submitted = st.form_submit_button("✨ Gợi ý phương pháp học", use_container_width=True)

    if submitted:
        if not subject:
            st.error("Vui lòng nhập môn học!")
        else:
            with st.spinner("AI đang phân tích..."):
                prompt = f"""Gợi ý 2-3 phương pháp học phù hợp nhất cho học sinh với thông tin:
Môn học: {subject}
Vấn đề: {problem or 'Muốn học hiệu quả hơn'}
Phong cách học: {style}

Với mỗi phương pháp (Pomodoro, Feynman, Spaced Repetition, Shadowing, Mind Map, Cornell Notes...):
1. Tên phương pháp
2. Tại sao phù hợp với bạn
3. Hướng dẫn áp dụng cụ thể (3-4 bước)

Trả lời bằng tiếng Việt, thực tế và dễ làm theo."""
                result = call_ai(prompt)
                st.session_state.method_result = result
                add_xp(5)

    if st.session_state.method_result:
        st.markdown("### 💡 Phương pháp gợi ý")
        colors = ["#7c6ff7", "#4ecdc4", "#ffb347"]
        sections = []
        current = None
        lines_buf = []

        for line in st.session_state.method_result.split('\n'):
            stripped = line.strip()
            is_title = (stripped.startswith('**') or stripped.startswith('##') or
                       (len(stripped) < 80 and stripped.endswith(':') and not stripped.startswith('-')))
            if is_title and stripped:
                if current:
                    sections.append((current, '\n'.join(lines_buf)))
                current = stripped.replace('**','').replace('#','').replace(':','').strip()
                lines_buf = []
            elif current and stripped:
                lines_buf.append(stripped.lstrip('-•* '))

        if current:
            sections.append((current, '\n'.join(lines_buf)))

        if sections:
            for i, (title, content) in enumerate(sections):
                color = colors[i % len(colors)]
                content_html = ''.join([f'<div style="font-size:13px;color:#8b90a8;line-height:1.8;padding:2px 0;">• {l}</div>' for l in content.split('\n') if l.strip()])
                st.markdown(f'<div class="method-card" style="border-left-color:{color};"><div class="method-title" style="color:{color};">{title}</div>{content_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="fm-card" style="white-space:pre-wrap;font-size:14px;line-height:1.8;">{st.session_state.method_result}</div>', unsafe_allow_html=True)

# ─── QUIZ ──────────────────────────────────────────────────────
elif st.session_state.page == "quiz":
    st.markdown("## ✍️ Tạo bài kiểm tra")
    st.caption("Dán tài liệu vào — AI tạo quiz để kiểm tra kiến thức")

    if not st.session_state.quiz_questions:
        with st.form("quiz_form"):
            material = st.text_area("📄 Nội dung tài liệu học", height=250,
                placeholder="Dán nội dung bài học vào đây...\nAI sẽ tạo 5 câu hỏi trắc nghiệm từ nội dung này.")
            submitted = st.form_submit_button("🎯 Tạo bài kiểm tra", use_container_width=True)

        if submitted:
            if len(material.strip()) < 30:
                st.error("Vui lòng dán đủ nội dung tài liệu!")
            else:
                with st.spinner("AI đang tạo câu hỏi..."):
                    prompt = f"""Tạo 5 câu hỏi trắc nghiệm tiếng Việt từ tài liệu sau.
Trả về ĐÚNG JSON format (không thêm gì khác, không markdown):
[{{"question":"...","options":["A. ...","B. ...","C. ...","D. ..."],"answer":"A","explain":"..."}}]

Tài liệu:
{material[:3000]}"""
                    result = call_ai(prompt)
                    try:
                        clean = result.strip().replace('```json','').replace('```','').strip()
                        questions = json.loads(clean)
                        if isinstance(questions, list) and len(questions) > 0:
                            st.session_state.quiz_questions = questions
                            st.session_state.quiz_index = 0
                            st.session_state.quiz_score = 0
                            st.session_state.quiz_done = False
                            st.session_state.quiz_answered = False
                            st.rerun()
                        else:
                            st.error("Không thể tạo câu hỏi. Thử lại nhé!")
                    except:
                        st.error("AI trả về định dạng không đúng. Thử lại!")

    elif st.session_state.quiz_done:
        score = st.session_state.quiz_score
        total = len(st.session_state.quiz_questions)
        pct = int(score / total * 100)
        emoji = "🏆" if pct >= 80 else "⭐" if pct >= 60 else "💪"
        msg = "Xuất sắc!" if pct >= 80 else "Khá tốt!" if pct >= 60 else "Cần cố gắng thêm!"

        st.markdown(f"""
        <div class="fm-card" style="text-align:center;padding:40px;">
          <div style="font-size:64px;margin-bottom:16px;">{emoji}</div>
          <div style="font-size:48px;font-weight:700;background:linear-gradient(90deg,#9d99ff,#6ee8df);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{score}/{total}</div>
          <div style="color:#8b90a8;font-size:18px;margin-top:8px;">{msg}</div>
          <div style="color:#555a70;font-size:14px;margin-top:4px;">+{score * 20} XP nhận được</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Làm lại", use_container_width=True):
                st.session_state.quiz_questions = []
                st.session_state.quiz_done = False
                st.rerun()
        with col2:
            if st.button("🏠 Về Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.session_state.quiz_questions = []
                st.rerun()

    else:
        questions = st.session_state.quiz_questions
        idx = st.session_state.quiz_index
        q = questions[idx]

        st.markdown(f'<span class="badge badge-mint">Câu {idx+1}/{len(questions)}</span>', unsafe_allow_html=True)
        st.progress((idx) / len(questions))
        st.markdown(f"### {q['question']}")

        if not st.session_state.quiz_answered:
            for opt in q['options']:
                if st.button(opt, key=f"opt_{opt}", use_container_width=True):
                    st.session_state.quiz_selected = opt[0]
                    st.session_state.quiz_answered = True
                    if opt[0] == q['answer']:
                        st.session_state.quiz_score += 1
                        add_xp(20)
                    st.rerun()
        else:
            selected = st.session_state.quiz_selected
            for opt in q['options']:
                is_correct = opt[0] == q['answer']
                is_selected = opt[0] == selected
                if is_correct:
                    st.success(f"✅ {opt}")
                elif is_selected:
                    st.error(f"❌ {opt}")
                else:
                    st.markdown(f'<div style="padding:8px 16px;border:1px solid rgba(255,255,255,0.1);border-radius:8px;margin:4px 0;color:#8b90a8;font-size:14px;">{opt}</div>', unsafe_allow_html=True)

            if selected == q['answer']:
                st.success("🎉 Chính xác!")
            else:
                st.error(f"Đáp án đúng: **{q['answer']}**")

            if 'explain' in q:
                st.info(f"💡 {q['explain']}")

            if st.button("Câu tiếp theo →", use_container_width=True):
                next_idx = idx + 1
                if next_idx >= len(questions):
                    st.session_state.quiz_done = True
                else:
                    st.session_state.quiz_index = next_idx
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None
                st.rerun()

# ─── CHAT ──────────────────────────────────────────────────────
elif st.session_state.page == "chat":
    st.markdown("## 💬 Tâm sự với AI")
    st.caption("Người bạn luôn lắng nghe, không phán xét")

    # Show chat history
    if not st.session_state.chat_history:
        st.markdown(f'<div class="chat-ai">Xin chào {st.session_state.name}! 🌱 Mình ở đây để lắng nghe bạn. Hôm nay bạn cảm thấy thế nào? Có điều gì muốn chia sẻ không?</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("", placeholder="Nhập tin nhắn...", label_visibility="collapsed")
        with col2:
            send = st.form_submit_button("Gửi", use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

        system = f"""Bạn là người bạn AI ấm áp, đồng cảm dành cho học sinh Việt Nam tên là {st.session_state.name}.
Bạn được huấn luyện về tâm lý học. Khi học sinh chia sẻ về áp lực, stress, trầm cảm, burnout:
- Lắng nghe thật sự, phản hồi bằng sự đồng cảm chân thành
- Không nói những lời sáo rỗng
- Đưa ra lời khuyên thực tế dựa trên tâm lý học
- Trả lời bằng tiếng Việt tự nhiên như bạn bè, tối đa 4 câu."""

        history_text = "\n".join([f"{'Học sinh' if m['role']=='user' else 'AI'}: {m['content']}"
                                   for m in st.session_state.chat_history[-10:]])

        with st.spinner(""):
            reply = call_ai(history_text, system_prompt=system, max_tokens=300)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Xóa lịch sử chat"):
            st.session_state.chat_history = []
            st.rerun()

# ─── LEADERBOARD ───────────────────────────────────────────────
elif st.session_state.page == "leaderboard":
    st.markdown("## 🏆 Bảng xếp hạng")
    st.caption("Cạnh tranh lành mạnh — chỉ chia sẻ điểm học tập, không dữ liệu cá nhân")

    mock = [
        {"name": "Minh Anh", "xp": 420, "streak": 12, "tasks": 35},
        {"name": "Tuấn Kiệt", "xp": 380, "streak": 9, "tasks": 28},
        {"name": st.session_state.name or "Bạn", "xp": st.session_state.xp, "streak": st.session_state.streak, "tasks": st.session_state.tasks_done},
        {"name": "Hải Yến", "xp": 180, "streak": 5, "tasks": 15},
        {"name": "Phúc Thịnh", "xp": 90, "streak": 3, "tasks": 8},
    ]
    mock.sort(key=lambda x: x["xp"], reverse=True)
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    for i, u in enumerate(mock):
        is_me = u["name"] == (st.session_state.name or "Bạn")
        border = "border:1px solid #7c6ff7;background:rgba(124,111,247,0.05);" if is_me else ""
        you_badge = '<span class="badge badge-purple">Bạn</span>' if is_me else ""
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;background:#1a1e2a;{border}
             border-radius:10px;padding:14px 16px;margin-bottom:8px;">
          <div style="font-size:20px;width:28px;text-align:center;">{medals[i]}</div>
          <div style="flex:1;font-size:14px;font-weight:500;">{u['name']} {you_badge}</div>
          <div style="display:flex;gap:16px;font-size:13px;color:#8b90a8;">
            <span>⭐ {u['xp']} XP</span>
            <span>🔥 {u['streak']} ngày</span>
            <span>✅ {u['tasks']}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**Tham gia nhóm học tập**")
    col1, col2 = st.columns([3, 1])
    with col1:
        group_code = st.text_input("", placeholder="Nhập mã nhóm...", label_visibility="collapsed")
    with col2:
        if st.button("Tham gia", use_container_width=True):
            if group_code:
                st.success(f"✅ Đã tham gia nhóm: {group_code}")
