from __future__ import annotations

import streamlit as st

from src.chat.conversation import Conversation, ChatMessage
from src.chat.provider import chat_completion


def _get_api_key() -> str:
    # Prefer Streamlit secrets, fall back to session input
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return st.session_state.get("gemini_api_key", "")


def render_chat_panel() -> None:
    if "conversation" not in st.session_state:
        st.session_state.conversation = Conversation()

    conv: Conversation = st.session_state.conversation

    st.subheader("Design Chat")
    st.caption("Talk to the design assistant. Gemini powers the replies.")

    # API key handling
    api_key = _get_api_key()
    if not api_key:
        with st.expander("Gemini API key required", expanded=True):
            key_input = st.text_input(
                "Enter Gemini API key",
                type="password",
                key="gemini_key_input",
                help="Get a key from Google AI Studio. Prefer setting it in .streamlit/secrets.toml as GEMINI_API_KEY.",
            )
            if key_input:
                st.session_state.gemini_api_key = key_input.strip()
                st.rerun()
        return

    # Message history
    for msg in conv.messages:
        with st.chat_message(msg.role):
            st.markdown(msg.content)
            col1, col2 = st.columns([1, 8])
            with col1:
                if st.button("Copy", key=f"copy_{msg.id}", help="Copy message"):
                    st.session_state[f"clipboard_{msg.id}"] = msg.content
                    st.toast("Copied to clipboard (use Ctrl+V / Cmd+V)")
            if msg.error:
                with col2:
                    if st.button("Retry", key=f"retry_{msg.id}"):
                        _retry_last(conv, api_key)
                        st.rerun()

    # Input
    prompt = st.chat_input("Describe the pattern you want or ask a design question...")
    if prompt:
        conv.add_user(prompt)
        with st.spinner("Thinking..."):
            reply, err = chat_completion(api_key, conv.to_provider_messages())
        if err:
            conv.add_assistant(err, error=True)
        else:
            conv.add_assistant(reply or "No response.")
        st.rerun()

    # Clear
    if conv.messages:
        if st.button("Clear conversation", use_container_width=False):
            conv.clear()
            st.rerun()


def _retry_last(conv: Conversation, api_key: str) -> None:
    # Remove the last error assistant message and re-call
    if conv.messages and conv.messages[-1].error:
        conv.messages.pop()
    last_user = conv.last_user_message()
    if not last_user:
        return
    reply, err = chat_completion(api_key, conv.to_provider_messages())
    if err:
        conv.add_assistant(err, error=True)
    else:
        conv.add_assistant(reply or "No response.")
