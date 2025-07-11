# app/main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pandas as pd
import uuid
import os
import json

from app.jd_question_generator import generate_screening_questions
from app.eligibility_checker import evaluate_candidate_answers
from app.db import save_job, load_jobs
from app.report_generator import generate_report

app = FastAPI()

JOBS_DB_PATH = "jobs.json"
JOBS_DB = load_jobs(JOBS_DB_PATH)
CANDIDATES_DB = {}
RESPONSES_DB = []

@app.post("/upload_data/")
async def upload_data(
    job_title: str = Form(...),
    jd_file: UploadFile = File(...),
    candidates_file: UploadFile = File(...)
):
    # Process JD
    jd_text = (await jd_file.read()).decode("utf-8")
    questions = generate_screening_questions(jd_text)
    job_id = str(uuid.uuid4())
    JOBS_DB[job_id] = {
        "job_title": job_title,
        "jd_text": jd_text,
        "questions": questions
    }
    save_job(JOBS_DB_PATH, jd_text, questions)

    # Process Candidates
    df = pd.read_csv(candidates_file.file)
    uploaded = 0
    for _, row in df.iterrows():
        cid = str(uuid.uuid4())
        CANDIDATES_DB[cid] = {
            "name": row['name'],
            "phone": row['phone'],
            "job_title": row['job_title'],
            "status": "Pending",
            "answers": {}
        }
        uploaded += 1

    return {
        "job_id": job_id,
        "questions": questions,
        "candidates_uploaded": uploaded
    }

@app.post("/submit_response/")
async def submit_response(candidate_id: str, answers: dict):
    candidate = CANDIDATES_DB.get(candidate_id)
    job_entry = next((j for j in JOBS_DB.values() if j['job_title'] == candidate['job_title']), None)
    result = evaluate_candidate_answers(answers, job_entry['jd_text'])
    candidate['status'] = result['status']
    candidate['answers'] = answers
    RESPONSES_DB.append({"candidate_id": candidate_id, **candidate, **result})
    return result

@app.get("/report/")
def get_report():
    return generate_report(RESPONSES_DB, JOBS_DB)
