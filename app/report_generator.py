# app/report_generator.py

import csv
import os
from datetime import datetime

def generate_report(candidates_db: dict, output_dir="reports") -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"hiring_report_{timestamp}.csv")

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Phone", "Job Title", "Status", "Reason", "Answers"])

        for candidate in candidates_db.values():
            writer.writerow([
                candidate.get("name", ""),
                candidate.get("phone", ""),
                candidate.get("job_title", ""),
                candidate.get("status", "Pending"),
                candidate.get("reason", ""),
                format_answers(candidate.get("answers", {}))
            ])

    return filepath

def format_answers(answer_dict):
    return "; ".join(f"{k}: {v}" for k, v in answer_dict.items())
