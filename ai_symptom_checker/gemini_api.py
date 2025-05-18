import requests

API_KEY = "AIzaSyBYAX7pr3w2kfQDcngsq8UihwZlrL4kNRg"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

def build_prompt(symptoms):
    return (
        f"Patient describes symptoms: '{symptoms}'.\n"
        "As a healthcare AI assistant, please do the following:\n"
        "1. Summarize the main symptoms.\n"
        "2. List likely medical condition(s).\n"
        "3. Recommend the best type of medical specialist for these symptoms.\n"
        "Respond using this structured format:\n"
        "Summary: <...>\n"
        "Conditions: <...>\n"
        "Specialist: <...>\n"
        "If the input is too vague, respond with clarifying questions."
    )

def analyze_symptoms(symptoms):
    prompt = build_prompt(symptoms)
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    try:
        response = requests.post(API_URL, json=body, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        try:
            output = data['candidates'][0]['content']['parts'][0]['text']
            summary, conditions, specialist = "N/A", "N/A", "N/A"
            for line in output.split("\n"):
                if line.lower().startswith("summary:"):
                    summary = line.partition(":")[2].strip()
                elif line.lower().startswith("conditions:"):
                    conditions = line.partition(":")[2].strip()
                elif line.lower().startswith("specialist:"):
                    specialist = line.partition(":")[2].strip()
            if summary.lower().startswith("can you") or "clarify" in summary.lower():
                return {"error": summary}
            return {
                "summary": summary,
                "conditions": conditions,
                "specialist": specialist
            }
        except Exception as parse_error:
            return {"error": f"Could not parse Gemini API response: {parse_error}\nRaw output: {data}"}
    except Exception as api_error:
        return {"error": f"API error: {api_error}"}
