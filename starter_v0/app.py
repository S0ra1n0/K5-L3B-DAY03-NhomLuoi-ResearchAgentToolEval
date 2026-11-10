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

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)

st.set_page_config(
    page_title="AI Research Agent — Nhóm Lười (v3)",
    page_icon="🤖",
    layout="wide",
)

# Load artifacts
system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
tools_path = ARTIFACTS_DIR / "tools.yaml"

system_prompt = system_prompt_path.read_text(encoding="utf-8")
tool_declarations = load_tool_declarations(tools_path)
openai_tools = to_openai_tools(tool_declarations)
artifact_version = build_artifact_version("v3", system_prompt_path, tools_path)

# Sidebar
st.sidebar.title("🤖 Research Agent")
st.sidebar.markdown("**Nhóm Lười** — Lab C401 Tool-Calling")

# Version card (C6 requirement: show artifact_version)
st.sidebar.subheader("📌 Artifact Version")
st.sidebar.info(
    f"**Version:** `{artifact_version.artifact_version}`\n\n"
    f"- **Prompt:** `{artifact_version.prompt_hash}`\n"
    f"- **Tools:** `{artifact_version.tools_hash}`"
)

# Settings
st.sidebar.subheader("⚙️ Cấu hình")
provider_name = st.sidebar.selectbox("Provider", ["openrouter", "openai", "gemini", "anthropic", "ollama"], index=0)
default_model = "openai/gpt-4o-mini" if provider_name == "openrouter" else ""
model_name = st.sidebar.text_input("Model (để trống nếu dùng mặc định)", value=default_model)
history_window = st.sidebar.slider("History window", min_value=1, max_value=10, value=5)
max_tool_rounds = st.sidebar.slider("Max tool rounds", min_value=1, max_value=6, value=4)

if st.sidebar.button("🧹 Xóa hội thoại (Reset)", use_container_width=True):
    st.session_state.messages = []
    st.session_state.history = []
    st.rerun()

# Sample queries (A3)
st.sidebar.subheader("💡 Câu hỏi mẫu (A3)")
sample_queries = [
    "Tin tức AI hôm nay có gì nổi bật?",
    "Repo openai/whisper trên GitHub hiện có bao nhiêu sao?",
    "Tóm tắt bài viết này hộ mình",
    "Tìm paper arXiv về retrieval augmented generation",
    "Đăng bản tin AI hôm nay lên Telegram giúp mình",
]

selected_query = None
for q in sample_queries:
    if st.sidebar.button(q, key=f"sample_{q}", use_container_width=True):
        selected_query = q

# Main UI
st.title("🤖 AI Research Agent — Nhóm Lười")
st.caption(f"Trợ lý nghiên cứu đa nguồn (arXiv, Twitter/X, GitHub, Web news). Phiên bản: `{artifact_version.artifact_version}`")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            # Display tool calls & results if any (C6 requirement: show tool name, args, results, including errors)
            tool_events = msg.get("tool_events", [])
            if tool_events:
                with st.expander(f"🛠️ Đã thực thi {len(tool_events)} tool call(s)", expanded=True):
                    for idx, event in enumerate(tool_events, start=1):
                        tool_name = event.get("tool", "unknown")
                        args = event.get("args", {})
                        result = event.get("result", {})

                        has_error = False
                        if isinstance(result, dict) and ("error" in result or "message" in result and "error" in str(result).lower()):
                            has_error = True

                        header = f"**#{idx} Tool:** `{tool_name}`" + (" ❌ *(Có lỗi)*" if has_error else " ✅")
                        st.markdown(header)
                        st.markdown("**Arguments:**")
                        st.json(args)
                        st.markdown("**Result / Error:**")
                        if has_error:
                            st.error(f"Lỗi khi thực thi `{tool_name}`:")
                            st.json(result)
                        else:
                            st.json(result)
                        st.divider()

            # Status banner if waiting for user (clarify)
            if msg.get("status") == "waiting_for_user":
                st.warning("⏳ **Agent đang chờ xác nhận / thông tin bổ sung:**")

            st.markdown(msg["content"])
        else:
            st.markdown(msg["content"])

# Handle user input
user_input = st.chat_input("Nhập yêu cầu của bạn...")
if selected_query:
    user_input = selected_query

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare messages
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": user_input},
    ]

    # Run agent loop
    with st.chat_message("assistant"):
        with st.spinner("Agent đang xử lý và gọi tool..."):
            try:
                provider = make_provider(provider_name)
                active_model = model_name.strip() or None
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

                if tool_events:
                    with st.expander(f"🛠️ Đã thực thi {len(tool_events)} tool call(s)", expanded=True):
                        for idx, event in enumerate(tool_events, start=1):
                            tool_name = event.get("tool", "unknown")
                            args = event.get("args", {})
                            result_data = event.get("result", {})

                            has_error = False
                            if isinstance(result_data, dict) and ("error" in result_data or "message" in result_data and "error" in str(result_data).lower()):
                                has_error = True

                            header = f"**#{idx} Tool:** `{tool_name}`" + (" ❌ *(Có lỗi)*" if has_error else " ✅")
                            st.markdown(header)
                            st.markdown("**Arguments:**")
                            st.json(args)
                            st.markdown("**Result / Error:**")
                            if has_error:
                                st.error(f"Lỗi khi thực thi `{tool_name}`:")
                                st.json(result_data)
                            else:
                                st.json(result_data)
                            st.divider()

                if status == "waiting_for_user":
                    st.warning("⏳ **Agent đang chờ xác nhận / thông tin bổ sung:**")

                st.markdown(assistant_text)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tool_events": tool_events,
                    "status": status,
                })
                st.session_state.history.append({"role": "user", "content": user_input})
                st.session_state.history.append({"role": "assistant", "content": assistant_text})

            except Exception as exc:
                error_msg = f"❌ Lỗi: {type(exc).__name__}: {str(exc)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "tool_events": [],
                    "status": "provider_error",
                })
