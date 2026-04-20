import os
import requests


def main() -> None:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Environment variable MISTRAL_API_KEY is missing.")

    url = "https://api.mistral.ai/v1/chat/completions"

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "user",
                "content": "Hello, Mistral!"
            }
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=30
        )

        print("Status code:", response.status_code)
        print("Response body:", response.text)

        response.raise_for_status()

    except requests.Timeout as exc:
        raise TimeoutError("Request to Mistral API timed out.") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Request to Mistral API failed: {exc}") from exc


if __name__ == "__main__":
    main()