import os
import requests
from dotenv import load_dotenv


def main():
    load_dotenv(override=True)
    key = os.getenv("PERPLEXITY_API_KEY")
    if not key:
        print("PERPLEXITY_API_KEY not set")
        return

    print(f"Key Loaded: {key[:10]}...")
    print(f"Key Length: {len(key)}")

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar-pro",
                "messages": [{"role": "user", "content": "ping"}],
            },
            timeout=30,
        )
        print(f"Status Code: {response.status_code}")
        print("Response Text:")
        print(response.text)
    except requests.RequestException as exc:
        print(f"Connection Error: {exc}")


if __name__ == "__main__":
    main()
