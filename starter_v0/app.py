from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from env_loader import load_lab_env
from chat import run_model_tool_loop, trim_history
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version

# -----------------------------------------------------------------------------
# 1. Khởi tạo môi trường & Cấu hình Streamlit
# -----------------------------------------------------------------------------
ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)

st.set_page_config(
    page_title="AI Research Agent — Nhóm Lười (v3)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 2. CSS Tùy biến Hiện đại (Dark Mode / AI Product Style)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Font chữ mặc định */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Ẩn các nút deploy và menu thừa của Streamlit */
[data-testid="stToolbar"] {
    display: none !important;
}
#MainMenu, footer {
    visibility: hidden;
}

/* Giới hạn độ rộng vùng chat chính giữa, căn lề thanh thoát */
.main .block-container {
    max-width: 920px !important;
    padding-top: 1.8rem !important;
    padding-bottom: 5rem !important;
}

/* Header & Gradient Typography */
.hero-container {
    text-align: center;
    padding: 2.2rem 1rem 1.6rem 1rem;
    margin-bottom: 1.5rem;
    background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.12) 0%, transparent 70%);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.14);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #A5B4FC;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF 20%, #A5B4FC 60%, #6366F1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
    letter-spacing: -0.025em;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 0.98rem;
    line-height: 1.55;
    max-width: 640px;
    margin: 0 auto;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #0E131F !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07);
}

.sidebar-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #F8FAFC;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 2px;
}

.sidebar-badge {
    display: inline-block;
    padding: 2px 8px;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 6px;
    font-size: 0.75rem;
    color: #C7D2FE;
    font-weight: 600;
}

.sidebar-section-header {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    font-weight: 700;
    margin-top: 1.4rem;
    margin-bottom: 0.5rem;
}

.card-version {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 1rem;
}

.chip-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2px 7px;
    border-radius: 5px;
    color: #E2E8F0;
}

/* Empty State & Prompt Cards */
.empty-section-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.8rem;
    text-align: center;
}

/* Tool Event Box */
.tool-header-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    padding: 3px 8px;
    border-radius: 6px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #C7D2FE;
    font-weight: 600;
}

.tool-badge-success {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34D399;
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 600;
}

.tool-badge-error {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #F87171;
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 600;
}

/* Banner Trạng thái (Waiting / Error) */
.waiting-banner {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.45);
    color: #FDE68A;
    padding: 12px 18px;
    border-radius: 12px;
    margin: 12px 0;
    font-size: 0.92rem;
    font-weight: 500;
    animation: banner-pulse 2s infinite ease-in-out;
}

@keyframes banner-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.85; transform: scale(0.998); }
}

.error-banner {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.45);
    color: #FCA5A5;
    padding: 12px 18px;
    border-radius: 12px;
    margin: 12px 0;
    font-size: 0.92rem;
}

/* Chat bubble styling */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 12px 18px;
    margin-bottom: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Nút bấm Reset màu đỏ nhạt */
div[data-testid="stSidebar"] button:has(div:contains("Reset")),
div[data-testid="stSidebar"] button:has(div:contains("Xóa hội thoại")) {
    background-color: rgba(239, 68, 68, 0.08) !important;
    border: 1px solid rgba(239, 68, 68, 0.35) !important;
    color: #FCA5A5 !important;
}
div[data-testid="stSidebar"] button:has(div:contains("Reset")):hover,
div[data-testid="stSidebar"] button:has(div:contains("Xóa hội thoại")):hover {
    background-color: rgba(239, 68, 68, 0.18) !important;
    border-color: #EF4444 !important;
    color: #FFFFFF !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Nạp Artifacts & Định danh Phiên bản (v3)
# -----------------------------------------------------------------------------
system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_path = ARTIFACTS_DIR / "tools.yaml"

system_prompt = system_prompt_path.read_text(encoding="utf-8")
tool_declarations = load_tool_declarations(tools_path)
openai_tools = to_openai_tools(tool_declarations)
artifact_version = build_artifact_version("v3", system_prompt_path, tools_path)

# Danh sách 5 câu hỏi mẫu chuẩn (A3)
SAMPLE_QUERIES = [
    "Tin tức AI hôm nay có gì nổi bật?",
    "Repo openai/whisper trên GitHub hiện có bao nhiêu sao?",
    "Tóm tắt bài viết này hộ mình",
    "Tìm paper arXiv về retrieval augmented generation",
    "Đăng bản tin AI hôm nay lên Telegram giúp mình",
]

# -----------------------------------------------------------------------------
# 4. Các Hàm Helper Giao Diện & Báo Cáo
# -----------------------------------------------------------------------------
def is_tool_error(result: Any) -> bool:
    """Kiểm tra xem kết quả của tool có chứa lỗi hay không (đảm bảo đúng thứ tự ưu tiên toán tử)."""
    if not isinstance(result, dict):
        return False
    return bool(("error" in result) or ("message" in result and "error" in str(result).lower()))


def render_tool_events(tool_events: list[dict[str, Any]]) -> None:
    """Hiển thị toàn bộ các tool calls, arguments và kết quả (kể cả lỗi) theo chuẩn C6."""
    if not tool_events:
        return

    total = len(tool_events)
    errors = sum(1 for e in tool_events if is_tool_error(e.get("result")))
    successes = total - errors

    # Tiêu đề expander có thống kê rõ ràng số lượng thành công / lỗi
    expander_title = f"🛠️ Đã thực thi {total} tool call(s) · {successes} thành công"
    if errors > 0:
        expander_title += f" · {errors} lỗi ❌"

    with st.expander(expander_title, expanded=True):
        for idx, event in enumerate(tool_events, start=1):
            tool_name = event.get("tool", "unknown")
            args = event.get("args", {})
            result = event.get("result", {})
            has_error = is_tool_error(result)

            status_badge = (
                '<span class="tool-badge-error">❌ Thất bại / Lỗi</span>'
                if has_error
                else '<span class="tool-badge-success">✅ Thành công</span>'
            )
            tool_chip = f'<span class="tool-header-badge">#{idx} {tool_name}</span>'

            st.markdown(
                f"<div style='display: flex; justify-content: space-between; align-items: center; margin: 8px 0 10px 0;'>"
                f"{tool_chip} {status_badge}</div>",
                unsafe_allow_html=True,
            )

            # Chia 2 tabs gọn gàng: Tham số đầu vào (Args) và Kết quả đầu ra (Result)
            tab_args, tab_res = st.tabs(["📋 Arguments (JSON)", "📦 Result / Output"])
            with tab_args:
                st.json(args)
            with tab_res:
                if has_error:
                    st.error(f"⚠️ Phát hiện lỗi khi thực thi tool `{tool_name}` (Không che giấu lỗi):")
                    st.json(result)
                else:
                    st.json(result)

            if idx < total:
                st.markdown("<hr style='border: none; border-top: 1px dashed rgba(255,255,255,0.1); margin: 12px 0;'>", unsafe_allow_html=True)


def render_status_banner(status: str, content: str = "") -> None:
    """Hiển thị banner trạng thái trực quan: waiting_for_user (vàng) hoặc provider_error (đỏ)."""
    if status == "waiting_for_user":
        st.markdown(
            """
            <div class="waiting-banner">
                <span style="font-size: 1.3rem;">⏳</span>
                <div>
                    <strong>Agent đang chờ thông tin bổ sung / xác nhận từ bạn:</strong>
                    <div style="font-size: 0.85rem; opacity: 0.9; margin-top: 2px;">
                        Vui lòng nhập phản hồi hoặc xác nhận vào ô bên dưới để tiếp tục luồng xử lý.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif status == "provider_error":
        st.markdown(
            f"""
            <div class="error-banner">
                <span style="font-size: 1.3rem;">❌</span>
                <div>
                    <strong>Lỗi kết nối Provider / Model:</strong>
                    <div style="font-size: 0.85rem; opacity: 0.9; margin-top: 2px;">{content}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_empty_state() -> str | None:
    """Hiển thị màn hình chào mừng (empty state) khi chưa có hội thoại, tích hợp sẵn thẻ gợi ý."""
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="hero-badge">🚀 Phiên bản {artifact_version.artifact_version}</div>
            <div class="hero-title">AI Research Agent</div>
            <div class="hero-subtitle">
                Trợ lý nghiên cứu đa nguồn (arXiv, Twitter/X, GitHub, Web news).<br>
                Tích hợp guardrail an toàn, ranh giới ghi dữ liệu và xử lý gọi tool đa bước tự động.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="empty-section-title">💡 Gợi ý câu hỏi bắt đầu nhanh (A3)</div>', unsafe_allow_html=True)

    # Hiển thị 5 thẻ câu hỏi mẫu dạng lưới
    col1, col2 = st.columns(2)
    selected_query = None

    with col1:
        if st.button("📰 " + SAMPLE_QUERIES[0], key="empty_q0", use_container_width=True):
            selected_query = SAMPLE_QUERIES[0]
        if st.button("⭐ " + SAMPLE_QUERIES[1], key="empty_q1", use_container_width=True):
            selected_query = SAMPLE_QUERIES[1]
        if st.button("🔗 " + SAMPLE_QUERIES[2], key="empty_q2", use_container_width=True):
            selected_query = SAMPLE_QUERIES[2]

    with col2:
        if st.button("📚 " + SAMPLE_QUERIES[3], key="empty_q3", use_container_width=True):
            selected_query = SAMPLE_QUERIES[3]
        if st.button("✈️ " + SAMPLE_QUERIES[4], key="empty_q4", use_container_width=True):
            selected_query = SAMPLE_QUERIES[4]

    return selected_query


def render_sidebar() -> tuple[str, str | None, int, int, str | None]:
    """Hiển thị toàn bộ Sidebar chuẩn giao diện AI Product."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-title">
                🤖 Research Agent
                <span class="sidebar-badge">Nhóm Lười</span>
            </div>
            <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">Lab C401 Tool-Calling · Lớp L3B</div>
            """,
            unsafe_allow_html=True,
        )

        # 1. Thẻ Artifact Version (Tiêu chí C6 bắt buộc)
        st.markdown('<div class="sidebar-section-header">📌 Định danh Artifact v3</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="card-version">
                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Artifact Version</div>
                <div style="font-size: 0.92rem; font-weight: 700; color: #A5B4FC; margin: 2px 0 8px 0; word-break: break-all;">
                    {artifact_version.artifact_version}
                </div>
                <div style="display: flex; flex-direction: column; gap: 4px;">
                    <div><span style="color: #64748B; font-size: 0.75rem;">Prompt:</span> <span class="chip-mono">{artifact_version.prompt_hash}</span></div>
                    <div><span style="color: #64748B; font-size: 0.75rem;">Tools:</span> <span class="chip-mono">{artifact_version.tools_hash}</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Cấu hình Model & Provider
        st.markdown('<div class="sidebar-section-header">⚙️ Cấu hình Mô hình</div>', unsafe_allow_html=True)
        provider_name = st.selectbox(
            "Provider",
            ["openrouter", "openai", "gemini", "anthropic", "ollama"],
            index=0,
            help="Chọn provider gọi API cho agent",
        )
        default_model = "openai/gpt-4o-mini" if provider_name == "openrouter" else ""
        model_name = st.text_input("Model (để trống nếu dùng mặc định)", value=default_model)
        active_model = model_name.strip() or None

        history_window = st.slider("Lịch sử hội thoại (History Window)", min_value=1, max_value=10, value=5)
        max_tool_rounds = st.slider("Số vòng Tool tối đa (Max Rounds)", min_value=1, max_value=6, value=4)

        # Nút Reset hội thoại
        if st.button("🧹 Xóa hội thoại (Reset)", use_container_width=True):
            st.session_state.messages = []
            st.session_state.history = []
            st.rerun()

        # 3. Danh sách câu hỏi mẫu A3
        st.markdown('<div class="sidebar-section-header">💡 Câu hỏi mẫu (A3)</div>', unsafe_allow_html=True)
        selected_query = None
        for q in SAMPLE_QUERIES:
            if st.button(q, key=f"side_sample_{q}", use_container_width=True):
                selected_query = q

        return provider_name, active_model, history_window, max_tool_rounds, selected_query


# -----------------------------------------------------------------------------
# 5. Khởi tạo Session State (Bảo toàn 100% cấu trúc logic)
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# Vẽ Sidebar và thu thập cấu hình
provider_name, active_model, history_window, max_tool_rounds, sidebar_selected_query = render_sidebar()

# -----------------------------------------------------------------------------
# 6. Hiển thị Giao diện Chat Chính
# -----------------------------------------------------------------------------
# Nếu chưa có tin nhắn nào -> Hiện Empty State (Màn hình Hero + 5 thẻ gợi ý)
empty_state_selected_query = None
if len(st.session_state.messages) == 0:
    empty_state_selected_query = render_empty_state()

# Hiển thị lại toàn bộ lịch sử tin nhắn trong session
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            # 1. Hiển thị Tool calls và kết quả chi tiết
            render_tool_events(msg.get("tool_events", []))

            # 2. Hiển thị Banner nếu đang chờ xác nhận hoặc có lỗi
            render_status_banner(msg.get("status", "answered"), msg.get("content", ""))

            # 3. Hiển thị văn bản trả lời của Assistant
            st.markdown(msg["content"])
        else:
            st.markdown(msg["content"])

# -----------------------------------------------------------------------------
# 7. Xử lý Input & Vòng lặp Agent Tool Loop
# -----------------------------------------------------------------------------
user_input = st.chat_input("Nhập yêu cầu nghiên cứu của bạn...")

# Ưu tiên câu hỏi mẫu được chọn từ Sidebar hoặc Empty State
chosen_query = sidebar_selected_query or empty_state_selected_query
if chosen_query:
    user_input = chosen_query

if user_input:
    # 1. Ghi nhận và hiển thị tin nhắn của User
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Chuẩn bị ngữ cảnh cho Agent
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": user_input},
    ]

    # 3. Kích hoạt luồng Agent gọi Tool
    with st.chat_message("assistant"):
        with st.spinner("Agent đang suy nghĩ và thực thi công cụ..."):
            try:
                provider = make_provider(provider_name)
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=active_model,
                    max_tool_rounds=max_tool_rounds,
                )

                tool_events = result.get("tool_events", [])
                assistant_text = result.get("assistant_text", "")
                status = result.get("status", "answered")

                # Hiển thị kết quả công cụ
                render_tool_events(tool_events)

                # Hiển thị banner trạng thái nếu cần
                render_status_banner(status, assistant_text)

                # Hiển thị câu trả lời cuối cùng
                st.markdown(assistant_text)

                # Lưu vào bộ nhớ phiên
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tool_events": tool_events,
                    "status": status,
                })
                st.session_state.history.append({"role": "user", "content": user_input})
                st.session_state.history.append({"role": "assistant", "content": assistant_text})

            except Exception as exc:
                error_msg = f"Lỗi hệ thống ({type(exc).__name__}): {str(exc)}"
                render_status_banner("provider_error", error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "tool_events": [],
                    "status": "provider_error",
                })
