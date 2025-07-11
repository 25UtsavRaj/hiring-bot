# app/twilio_handler.py

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
import requests
import os

from app.main import CANDIDATES_DB, JOBS_DB
from app.call_manager import (
    init_session, get_next_question, save_answer,
    is_complete, get_all_answers
)
from app.eligibility_checker import evaluate_candidate_answers
from app.whisper_transcriber import transcribe_audio

router = APIRouter()

@router.post("/twilio/voice")
async def handle_voice(request: Request):
    form = await request.form()
    caller = form.get("From")
    candidate_id = find_candidate_by_phone(caller)

    if not candidate_id:
        resp = VoiceResponse()
        resp.say("Candidate not recognized. Goodbye.")
        return PlainTextResponse(str(resp))

    candidate = CANDIDATES_DB[candidate_id]
    job_entry = next((j for j in JOBS_DB.values() if j["job_title"] == candidate["job_title"]), None)

    if not job_entry:
        resp = VoiceResponse()
        resp.say("No job found for this candidate.")
        return PlainTextResponse(str(resp))

    if not get_all_answers(candidate_id):
        init_session(candidate_id, job_entry["questions"])

    if is_complete(candidate_id):
        answers = get_all_answers(candidate_id)
        result = evaluate_candidate_answers(answers, job_entry["jd_text"])
        candidate["status"] = result["status"]
        candidate["answers"] = answers
        resp = VoiceResponse()
        resp.say("Thank you. Your answers have been recorded.")
        return PlainTextResponse(str(resp))

    question = get_next_question(candidate_id)

    resp = VoiceResponse()
    resp.say(question["question"])
    resp.record(
        action=f"/twilio/collect?cid={candidate_id}&field={question['field']}",
        maxLength=10,
        playBeep=True,
        trim="trim-silence"
    )
    return PlainTextResponse(str(resp))

@router.post("/twilio/collect")
async def collect_answer(request: Request):
    form = await request.form()
    candidate_id = request.query_params.get("cid")
    field = request.query_params.get("field")
    recording_url = form.get("RecordingUrl", "")

    audio_path = download_audio(recording_url, candidate_id, field)
    transcript = transcribe_audio(audio_path)
    save_answer(candidate_id, field, transcript)

    resp = VoiceResponse()
    resp.redirect("/twilio/voice")
    return PlainTextResponse(str(resp))

def find_candidate_by_phone(phone):
    for cid, data in CANDIDATES_DB.items():
        if data["phone"].endswith(phone[-10:]):
            return cid
    return None

def download_audio(url, candidate_id, field):
    folder = f"recordings/{candidate_id}"
    os.makedirs(folder, exist_ok=True)
    path = f"{folder}/{field}.wav"
    audio = requests.get(url + ".wav")
    with open(path, "wb") as f:
        f.write(audio.content)
    return path
