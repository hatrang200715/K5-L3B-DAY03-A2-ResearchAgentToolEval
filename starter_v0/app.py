from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import json_text, now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
TRANSCRIPTS_DIR = ROOT / "transcripts"

load_lab_env(ROOT)

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="centered",
)


def make_transcript_id(version: str, provider: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    return "_".join([safe_slug(version), safe_slug(provider), timestamp])


def start_session(*, version: str, provider: str, model: str, max_tool_rounds: int) -> dict[str, Any]:
    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(TOOLS_PATH)
    openai_tools = to_openai_tools(tool_declarations)
    artifact_version = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    transcript_id = make_transcript_id(version, provider)
    transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"

    transcript: dict[str, Any] = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider,
        "model": model,
        "system_prompt": str(SYSTEM_PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "system_prompt_text": system_prompt,
        "tool_declarations": tool_declarations,
        "history_window": 5,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    write_transcript(transcript_path, transcript)

    return {
        "version": version,
        "provider": provider,
        "model": model,
        "max_tool_rounds": max_tool_rounds,
        "system_prompt": system_prompt,
        "openai_tools": openai_tools,
        "artifact_version": artifact_version,
        "history": [],
        "messages": [],
        "transcript": transcript,
        "transcript_path": transcript_path,
        "turn_index": 0,
    }


def show_tool_events(events: list[dict[str, Any]]) -> None:
    if not events:
        return

    with st.expander(f"Tool activity ({len(events)})", expanded=False):
        for index, event in enumerate(events, start=1):
            tool_name = event.get("tool", "unknown")
            args = event.get("args", {})
            result = event.get("result", {})
            st.markdown(f"**{index}. `{tool_name}`**")
            st.code(json_text(args, max_chars=4000), language="json")
            if isinstance(result, dict) and result.get("error"):
                message = result.get("message") or result.get("error")
                st.error(f"Tool error: {message}")
            st.code(json_text(result, max_chars=8000), language="json")


def render_message(message: dict[str, Any]) -> None:
    with st.chat_message(message["role"]):
        content = message.get("content", "")
        if message.get("status") == "provider_error":
            st.error(content)
        else:
            st.markdown(content)
        show_tool_events(message.get("tool_events", []))
        if message.get("status") == "waiting_for_user":
            st.caption("Waiting for your reply before continuing.")


st.title("🔎 Research Agent")
st.caption("Research across web and social sources using the tools declared for this project.")

with st.sidebar:
    st.header("Session settings")
    configured_provider = st.selectbox(
        "Provider",
        ["openrouter", "openai", "anthropic", "gemini", "ollama"],
        index=0,
    )
    configured_model = st.text_input(
        "Model",
        value="openrouter/free",
        help="Use openrouter/free to avoid paid OpenRouter models.",
    ).strip()
    configured_version = st.text_input(
        "Artifact version",
        value="v0",
        help="Set this to the version represented by the current prompt and tools, such as v1 or v3.",
    ).strip()
    configured_max_rounds = st.number_input(
        "Maximum tool rounds",
        min_value=1,
        max_value=10,
        value=4,
        step=1,
    )
    reload_requested = st.button("Start new chat / Reload artifacts", use_container_width=True)

if not configured_version:
    st.error("Artifact version cannot be empty.")
    st.stop()

if not configured_model:
    st.error("Model cannot be empty.")
    st.stop()

if "agent_session" not in st.session_state or reload_requested:
    try:
        st.session_state.agent_session = start_session(
            version=configured_version,
            provider=configured_provider,
            model=configured_model,
            max_tool_rounds=int(configured_max_rounds),
        )
    except Exception as exc:
        st.error(f"Could not load the agent artifacts: {type(exc).__name__}: {exc}")
        st.stop()

session = st.session_state.agent_session

requested_config = (
    configured_version,
    configured_provider,
    configured_model,
    int(configured_max_rounds),
)
active_config = (
    session["version"],
    session["provider"],
    session["model"],
    session["max_tool_rounds"],
)
if requested_config != active_config:
    st.info("Settings changed. Click “Start new chat / Reload artifacts” to apply them.")

artifact_version = session["artifact_version"]
with st.sidebar:
    st.divider()
    st.caption("Active artifact snapshot")
    st.code(artifact_version.artifact_version, language=None)
    st.caption(f"Prompt: `{artifact_version.prompt_hash[:12]}`")
    st.caption(f"Tools: `{artifact_version.tools_hash[:12]}`")
    st.caption(f"Transcript: `{session['transcript_path'].name}`")

for saved_message in session["messages"]:
    render_message(saved_message)

user_text = st.chat_input("Ask the research agent…")
if user_text:
    user_message = {"role": "user", "content": user_text}
    session["messages"].append(user_message)
    render_message(user_message)

    session["turn_index"] += 1
    turn_record: dict[str, Any] = {
        "turn_index": session["turn_index"],
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    messages = [
        {"role": "system", "content": session["system_prompt"]},
        *trim_history(session["history"], 5),
        {"role": "user", "content": user_text},
    ]

    try:
        with st.spinner("Researching…"):
            provider = make_provider(session["provider"])
            result = run_model_tool_loop(
                provider=provider,
                messages=messages,
                tools=session["openai_tools"],
                model=session["model"],
                max_tool_rounds=session["max_tool_rounds"],
            )

        assistant_text = result.get("assistant_text") or "The agent returned no text."
        assistant_message = {
            "role": "assistant",
            "content": assistant_text,
            "status": result.get("status", "answered"),
            "tool_events": result.get("tool_events", []),
        }
        session["messages"].append(assistant_message)
        render_message(assistant_message)

        session["history"].append({"role": "user", "content": user_text})
        session["history"].append({"role": "assistant", "content": assistant_text})
        turn_record.update(result)
    except Exception as exc:
        error_text = f"{type(exc).__name__}: {exc}"
        assistant_message = {
            "role": "assistant",
            "content": error_text,
            "status": "provider_error",
            "tool_events": [],
        }
        session["messages"].append(assistant_message)
        render_message(assistant_message)
        turn_record.update({
            "status": "provider_error",
            "error": error_text,
        })

    turn_record["ended_at"] = now_iso()
    session["transcript"]["turns"].append(turn_record)
    write_transcript(session["transcript_path"], session["transcript"])
