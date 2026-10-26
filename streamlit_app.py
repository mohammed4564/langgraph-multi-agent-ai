import re
import streamlit as st
from core.workflow import build_workflow

st.set_page_config(
    page_title="Multi-Agent AI",
    page_icon="🤖",
    layout="wide",
)


def make_report_text() -> str:
    """Build a plain-text transcript of the whole conversation."""
    lines = []
    for msg in st.session_state.history:
        role = "You" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}:\n{msg['content']}\n")
        lines.append("-" * 60)
    return "\n".join(lines)

# ---- Simple font + width ----
st.markdown("""
<style>
    html, body, [class*="css"] { font-size: 19px; }

    .block-container {
        max-width: 100% !important;
        padding: 1.5rem 2.5rem !important;
    }

    [data-testid="stChatMessage"] {
        padding: 1rem 1.25rem !important;
        border-radius: 14px !important;
        margin-bottom: 0.75rem !important;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }
    [data-testid="stChatMessage"] code {
        font-size: 1.02rem !important;
    }
    [data-testid="stChatMessage"] pre {
        font-size: 1.02rem !important;
        border-radius: 12px !important;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 1.1rem !important;
    }

    section[data-testid="stSidebar"] * {
        font-size: 1.02rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ---- Cached workflow ----
@st.cache_resource
def get_app():
    return build_workflow()

# ---- Header ----
st.title("🤖 Multi-Agent AI System")
st.caption("LangGraph + Ollama + Python")

if st.session_state.get("history"):
    st.download_button(
        label="⬇️ Download full report (.txt)",
        data=make_report_text(),
        file_name="multi_agent_report.txt",
        mime="text/plain",
        use_container_width=False,
    )

# ---- Sidebar (light, minimal) ----
st.sidebar.header("Available Agents")
st.sidebar.write("🗄️ SQL Agent")
st.sidebar.write("🔍 Data Quality Agent")
st.sidebar.write("📊 Reporting Agent")
st.sidebar.divider()

PLACEHOLDER = "Select a sample question..."
sample_questions = [
    PLACEHOLDER,
    "Write a SQL query to find duplicate CustomerIDs",
    "Write SQL to count customers by city",
    "Check customer data for missing values",
    "Check customer data for duplicate records",
    "Generate a data quality report for Customers",
    "Explain the Bronze, Silver, Gold architecture",
    "How do I clean data using PySpark?",
]
selected_question = st.sidebar.selectbox("📌 Sample Questions", sample_questions)

# ---- Session state ----
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""
if "last_sample" not in st.session_state:
    st.session_state.last_sample = PLACEHOLDER

if selected_question != PLACEHOLDER and selected_question != st.session_state.last_sample:
    st.session_state.selected_question = selected_question
st.session_state.last_sample = selected_question

# ---- Render history ----
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---- Input ----
question = st.chat_input("Ask your data engineering question...")

if not question and st.session_state.selected_question:
    question = st.session_state.selected_question
    st.session_state.selected_question = ""

# ---- Helpers ----
def format_response(text: str) -> str:
    if "```" in text:
        return text
    match = re.search(r"(?is)\bSELECT\b.+?;", text)
    if match:
        sql = match.group(0).strip()
        return text.replace(sql, f"```sql\n{sql}\n```")
    return text





# ---- Run ----
if question:
    st.session_state.history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Agent is working..."):
            try:
                result = get_app().invoke({
                    "user_request": question,
                    "agent": "",
                    "response": "",
                })

                agent = result.get("selected_agent", "unknown")
                response = result.get("result", str(result))
                response = format_response(response)

                st.info(f"Selected agent: {agent}")
                st.markdown(response)

                    # ⬇️ per-message download
                st.download_button(
                    label="⬇️ Download this answer",
                    data=response,
                    file_name=f"report_{len(st.session_state.history)}.txt",
                    mime="text/plain",
                    key=f"dl_{len(st.session_state.history)}",
                )

                st.session_state.history.append({
                    "role": "assistant",
                    "content": response,
                })
            except Exception as e:
                st.error(str(e))
                st.session_state.history.append({
                    "role": "assistant",
                    "content": f"⚠️ Error: {e}",
                })