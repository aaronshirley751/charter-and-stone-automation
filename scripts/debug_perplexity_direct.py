import os
import requests
from dotenv import load_dotenv


def main():
    load_dotenv()
    key = os.getenv("PERPLEXITY_API_KEY")
    if not key:
        print("PERPLEXITY_API_KEY not set")
        return

    print(f"Checking Key: {key[:5]}...")

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar",
                "messages": [{"role": "user", "content": "Hello World"}],
            },
            timeout=30,
        )
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(response.text)
    except requests.RequestException as exc:
        print(f"Connection Error: {exc}")


if __name__ == "__main__":
    main()
