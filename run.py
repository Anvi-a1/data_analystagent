import sys
import requests

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <base_url>")
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    api_url = f"{base_url}/api/"

    # The grader will place questions.txt and other files in the working directory
    files = {}
    try:
        files["questions_txt"] = ("questions.txt", open("questions.txt", "rb"), "text/plain")
    except FileNotFoundError:
        print("Error: questions.txt not found in current directory")
        sys.exit(1)

    # Add other optional files if they exist (like edges.csv, metadata.json, etc.)
    optional_files = ["edges.csv", "metadata.json"]
    for fname in optional_files:
        try:
            files["files"] = (fname, open(fname, "rb"))
        except FileNotFoundError:
            continue

    # POST request to your FastAPI /api/ endpoint
    resp = requests.post(api_url, files=files)

    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        print(f"API request failed: {e} - {resp.text}")
        sys.exit(1)

    # Print the JSON response exactly (grader reads this)
    print(resp.text)


if __name__ == "__main__":
    main()
