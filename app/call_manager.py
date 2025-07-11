# app/call_manager.py

# Manages per-candidate question flow during voice interaction

SESSION_STORE = {}  # candidate_id -> session

def init_session(candidate_id, questions):
    SESSION_STORE[candidate_id] = {
        "index": 0,
        "questions": questions,
        "answers": {}
    }

def get_next_question(candidate_id):
    session = SESSION_STORE.get(candidate_id)
    if not session:
        return None
    index = session["index"]
    if index < len(session["questions"]):
        return session["questions"][index]
    return None

def save_answer(candidate_id, field, answer):
    session = SESSION_STORE[candidate_id]
    session["answers"][field] = answer
    session["index"] += 1

def is_complete(candidate_id):
    session = SESSION_STORE.get(candidate_id)
    return session and session["index"] >= len(session["questions"])

def get_all_answers(candidate_id):
    return SESSION_STORE.get(candidate_id, {}).get("answers", {})
