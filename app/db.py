import json
import os

JOBS_PATH = "data/jobs.json"
CANDIDATES_PATH = "data/candidates.json"

def save_job(db_path, jd_text, questions):
    jobs = load_jobs(db_path)

    # Let's generate a safe string key from the jd_text (e.g., first 10 words)
    job_title = jd_text.strip().split()[:10]
    job_title = " ".join(job_title)

    jobs[job_title] = {
        "jd": jd_text,
        "questions": questions
    }

    with open(db_path, "w") as f:
        json.dump(jobs, f, indent=2)


def load_jobs(db_path):
    if not os.path.exists(db_path):
        return {}
    with open(db_path, "r") as f:
        return json.load(f)

