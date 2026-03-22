import streamlit as st
from prompts import get_prompt
from utils import ask_ai, extract_pdf_text, create_pdf

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Academic Assistant", layout="wide")

# ---------------- THEME SWITCH ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme_toggle = st.sidebar.toggle("🌗 Dark Mode", value=True)

if theme_toggle:
    st.session_state.theme = "dark"
else:
    st.session_state.theme = "light"

# ---------------- CSS STYLING ----------------
if st.session_state.theme == "dark":
    bg_color = "linear-gradient(135deg, #0f172a, #1e293b)"
    text_color = "#f1f5f9"
    card_bg = "#020617"
else:
    bg_color = "#f8fafc"
    text_color = "#0f172a"
    card_bg = "#ffffff"

st.markdown(f"""
<style>

.stApp {{
    background: {bg_color};
    color: {text_color};
}}

h1 {{
    text-align: center;
    color: #38bdf8;
}}

textarea {{
    border-radius: 12px !important;
    padding: 10px !important;
}}

.stButton>button {{
    background: linear-gradient(135deg, #22c55e, #4ade80);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}}

.stButton>button:hover {{
    transform: scale(1.05);
}}

.card {{
    background: {card_bg};
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
}}

.output-box {{
    background: {card_bg};
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #38bdf8;
}}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []
else:
    # Remove invalid entries (fix deployment error)
    st.session_state.history = [
        item for item in st.session_state.history
        if isinstance(item, dict) and "input" in item and "output" in item
    ]
# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 📚 AI Assistant")

task = st.sidebar.selectbox(
    "✨Select Task:",
    ["📝 Summarize", "😊 Sentiment", "❓ Q&A", "🌍 Translate", "⚖️ Compare", "🧠 Reasoning", "📄 Format", "📚 PDF Summarizer"]
)

clean_task = task.split(" ", 1)[1]

target_lang = ""
if clean_task == "Translate":
    target_lang = st.sidebar.text_input("🌐 Target Language")

st.sidebar.markdown("---")
st.sidebar.subheader("📜 Chat History")

for item in st.session_state.history[-3:]:
    st.sidebar.markdown(f"""
    📝 {item['input'][:30]}...  
    """)

# ---------------- TITLE ----------------
st.markdown("""
<h1>🤖 AI Smart Academic Assistant</h1>
<p style='text-align:center; color:#94a3b8;'>
Your intelligent study companion 🚀
</p>
""", unsafe_allow_html=True)

# ---------------- INPUT CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### ✍️ Enter Your Content")
user_input = st.text_area("", height=150)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
uploaded_file = None
if clean_task == "PDF Summarizer":
    uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

# ---------------- BUTTONS ----------------
col1, col2, col3 = st.columns([6,1,2])

with col1:
    generate = st.button("🚀 Generate Output")

with col3:
    download_pdf = st.button("📄 Download PDF")

# ---------------- GENERATE ----------------
if generate:

    with st.spinner("🤖 AI is thinking..."):

        if clean_task == "PDF Summarizer" and uploaded_file:
            pdf_text = extract_pdf_text(uploaded_file)
            prompt = f"Summarize this PDF content:\n{pdf_text}"
        else:
            prompt = get_prompt(clean_task, user_input, target_lang)

        result = ask_ai(prompt)

    # ✅ ALWAYS store both input + output
    st.session_state.history.append({
        "input": user_input,
        "output": result
    })

    # OUTPUT
    st.markdown('<div class="output-box">', unsafe_allow_html=True)
    st.markdown("### 📌 AI Response")
    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DOWNLOAD PDF ----------------
if st.session_state.history and download_pdf:

    last_entry = st.session_state.history[-1]

    if "input" in last_entry and "output" in last_entry:

        pdf_file = create_pdf(
            last_entry["input"],
            last_entry["output"]
        )

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF Report",
                data=f,
                file_name="AI_Report.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("⚠️ Please generate output first before downloading PDF.")
