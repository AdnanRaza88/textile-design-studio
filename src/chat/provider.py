from __future__ import annotations

from typing import Optional

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    HAS_LANGCHAIN = True
except Exception:
    HAS_LANGCHAIN = False


SYSTEM_PROMPT = """You are a professional textile design assistant inside Textile Design Studio.
You help users create and refine seamless SVG fabric patterns.
Be concise, practical and design-focused.
When the user asks for a new design, clearly describe the concept and note that the multi-agent pipeline will generate the actual SVG in a later step.
Do not invent SVG code unless the user explicitly asks for a small example snippet.
Never use emojis.
"""


def get_gemini_client(api_key: str, model: str = "gemini-2.0-flash"):
    if not HAS_LANGCHAIN:
        raise RuntimeError(
            "langchain-google-genai is not installed. Run: pip install langchain-google-genai"
        )
    if not api_key:
        raise ValueError("Gemini API key is required.")
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=0.7,
    )


def chat_completion(
    api_key: str,
    messages: list[dict],
    model: str = "gemini-2.0-flash",
) -> tuple[Optional[str], str]:
    """
    messages: list of {"role": "user"|"assistant"|"system", "content": str}
    Returns (reply_text, error_message)
    """
    try:
        llm = get_gemini_client(api_key, model=model)
        lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
            elif role == "system":
                lc_messages.append(SystemMessage(content=content))

        response = llm.invoke(lc_messages)
        text = getattr(response, "content", None) or str(response)
        return text.strip(), ""
    except Exception as exc:
        err = str(exc)
        if "API key" in err or "api_key" in err.lower() or "401" in err:
            return None, "Invalid or missing Gemini API key. Check your secrets."
        if "quota" in err.lower() or "rate" in err.lower() or "429" in err:
            return None, "Rate limit or quota exceeded. Please try again in a moment."
        if "connection" in err.lower() or "network" in err.lower() or "timeout" in err.lower():
            return None, "Network error. Check your internet connection and retry."
        return None, f"Provider error: {err}"
