import os
import anthropic
from dotenv import load_dotenv


def main():
    load_dotenv(override=True)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set")
        return

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=64,
            messages=[{"role": "user", "content": "Hello World"}],
        )
        print("Response:")
        print(response)
    except Exception as exc:
        print("Error:")
        print(repr(exc))
        raise


if __name__ == "__main__":
    main()
