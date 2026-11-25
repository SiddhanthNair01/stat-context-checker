import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()


def _setting(name: str) -> str:
    """Read a setting from Streamlit secrets (deployed) or .env (local)."""
    try:
        import streamlit as st
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing setting: {name}. Add it to .env")
    return value


MODEL_ID = _setting("GEMINI_MODEL")
client = genai.Client(api_key=_setting("GEMINI_API_KEY"))

RETRY_CODES = {429, 500, 503}  # rate limit, server error, overloaded


def ask(prompt: str, retries: int = 4) -> str:
    """Send a prompt to Gemini; wait and retry if it's busy."""
    for attempt in range(retries):
        try:
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            return response.text
        except errors.APIError as e:
            if e.code in RETRY_CODES and attempt < retries - 1:
                wait = 5 * 2 ** attempt  # 5s, 10s, 20s
                print(f"Gemini busy ({e.code}); retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise