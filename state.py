import json
from pathlib import Path
from config import STATE_FILE

DEFAULT_STATE = {"tickets": {}}

def load_state() -> dict:
    path = Path(STATE_FILE)
    if not path.exists():
        return DEFAULT_STATE.copy()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        state = DEFAULT_STATE.copy()
        state.update(data)
        if not isinstance(state.get("tickets"), dict):
            state["tickets"] = {}
        return state
    except (json.JSONDecodeError, OSError):
        return DEFAULT_STATE.copy()

def save_state(state: dict) -> None:
    Path(STATE_FILE).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
