import json
import os
import requests
import dotenv

dotenv.load_dotenv()


def test_api(url: str):
    api_endpoint = "http://127.0.0.1:8000/api/view/md/"
    headers = {
        'X-API-KEYS': json.dumps(
            {
                'X-CRAWLER-API-KEY': os.environ.get('CRAWLER_API_KEY'),
                'X-OPENAI-API-KEY': os.environ.get('OPENAI_API_KEY'),
            },
        )
    }
    print(headers)
    data = {"url": url}

    response = requests.post(api_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        print("Success! Here's the content:\n")
        print(response.json()["content"])
    else:
        print(f"Failed to fetch content. Status code: {response.status_code}")
        print("Response:", response.json())


if __name__ == "__main__":
    test_url = "https://www.example.com/"

    test_api(url=test_url)
