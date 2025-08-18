#!/usr/bin/env python3
import sys
import os
import json
import requests

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No API URL provided"}))
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    url = f"{base_url}/api/"

    # Default questions file (promptfoo will put the test question here)
    questions_file = "test_questions"
    if not os.path.exists(questions_file):
        # Fallback: look for any file with 'question' in its name
        for f in os.listdir("."):
            if "question" in f.lower():
                questions_file = f
                break

    if not os.path.exists(questions_file):
        print(json.dumps({"error": "No questions file found"}))
        sys.exit(1)

    # Prepare multipart form data
    files = {
        "questions_txt": (questions_file, open(questions_file, "rb"), "text/plain")
    }

    # Try to attach optional CSV/JSON files in current dir
    extra_files = []
    for f in os.listdir("."):
        if f.endswith((".csv", ".json")) and f != questions_file:
            extra_files.append(("files", (f, open(f, "rb"), "text/csv" if f.endswith(".csv") else "application/json")))
    if extra_files:
        for ef in extra_files:
            files[ef[0]] = ef[1]

    try:
        response = requests.post(url, files=files, timeout=180)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
