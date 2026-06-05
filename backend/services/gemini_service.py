import time
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

CLASSIFICATION_PROMPT = """
You are a lead qualification assistant for a company handling inbound business leads.

Read the lead message and:
1. Classify it as Hot, Warm, or Cold
2. Write a short professional reply of 1-2 sentences

Rules for the reply:
- Make it business-like and relevant to the lead's request
- Short greet, and reply. If relevent, reply like we have recorded your input and will reply accordingly.
- Do not explain your reasoning

Output format:
First line: Hot or Warm or Cold
Second line: the reply only

Lead message:
{message}
"""


def extract_classification(line: str) -> str:
    value = line.strip().lower()
    if value == "hot":
        return "Hot"
    if value == "warm":
        return "Warm"
    if value == "cold":
        return "Cold"
    raise ValueError(f"Invalid classification line: {line}")


def clean_reply(text: str) -> str:
    reply = " ".join(text.split()).strip()
    if not reply:
        raise ValueError("Reply is empty")
    return reply


def parse_llm_response(raw: str) -> dict:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]

    if len(lines) < 2:
        raise ValueError("LLM response must contain at least 2 non-empty lines")

    classification = extract_classification(lines[0])
    suggested_reply = clean_reply(" ".join(lines[1:]))

    return {
        "classification": classification,
        "suggested_reply": suggested_reply,
    }


def fallback_response() -> dict:
    return {
        "classification": "Warm",
        "suggested_reply": "Thank you for reaching out. We'll review your request and get back to you shortly."
    }


def classify_lead(message: str, max_retries: int = 3) -> dict:
    prompt = CLASSIFICATION_PROMPT.format(message=message.strip())
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=500,
                )
            )

            raw = response.text.strip()

            print(f"\n=== GEMINI RAW RESPONSE (attempt {attempt}) ===")
            print(raw)
            print("=== END RAW RESPONSE ===\n")

            parsed = parse_llm_response(raw)
            return parsed

        except Exception as e:
            last_error = e
            print(f"[gemini_service] Attempt {attempt} failed: {e}")

            if attempt < max_retries:
                time.sleep(attempt)   # simple backoff: 1s, 2s, 3s

    print(f"[gemini_service] All retries failed. Last error: {last_error}")
    return fallback_response()