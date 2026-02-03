import os
import anthropic
from dotenv import load_dotenv


def try_model(client: anthropic.Anthropic, model: str) -> bool:
    try:
        client.messages.create(
            model=model,
            max_tokens=32,
            messages=[{"role": "user", "content": "Hello World"}],
        )
        return True
    except Exception as exc:
        print(f"FAIL: {model} -> {exc}")
        return False


def main():
    load_dotenv(override=True)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set")
        return

    client = anthropic.Anthropic(api_key=api_key)

    candidates = [
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-haiku-20240307",
    ]

    for model in candidates:
        if try_model(client, model):
            print(f"WINNER: {model}")
            return

    print("No working model found")


if __name__ == "__main__":
    main()
