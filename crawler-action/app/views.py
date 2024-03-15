import json
import requests

from openai import OpenAI

from django.conf import settings

from markdownify import MarkdownConverter
from rest_framework.request import Request

from project import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import ContentSerializer


def is_valid_crawler_api_key(api_key: str) -> bool:
    return (api_key == settings.CRAWLER_DEFAULT_API_KEY)


def parse_api_key_from_headers(headers, key_name: str):
    return json.loads(headers.get('X-API-KEYS', "{}")).get(key_name)


class MarkdownConverterX(MarkdownConverter):
    def convert_style(self, el, text, convert_as_inline):
        return ""

    def convert_script(self, el, text, convert_as_inline):
        return ""


class BaseContentView(APIView):
    def fetch_content(self, url) -> (str | None):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

    def post(self, request, *args, **kwargs) -> Response:
        try:
            api_key = parse_api_key_from_headers(request.headers, key_name='X-CRAWLER-API-KEY')
        except Exception as e:
            data = {'error': f"Failed to parse API keys."}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not is_valid_crawler_api_key(api_key):
            api_key = f"{str(api_key)[0:4]}..." if api_key else "None"
            return Response({'error': f"Invalid API key: `{api_key}`"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContentSerializer(data=request.data)

        if serializer.is_valid():
            url = serializer.validated_data['url']
            content = self.fetch_content(url)
            if content is None:
                return Response({'error': "Failed to fetch URL content"}, status=status.HTTP_400_BAD_REQUEST)
            return self.handle_content(content, request=request)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_content(self, content: str, request: Request) -> Response:
        # Placeholder method to be overridden by subclasses
        raise NotImplementedError("Subclasses must implement this method")


class MarkdownView(BaseContentView):
    def handle_content(self, content: str, request: Request):
        markdown_content = MarkdownConverterX().convert(content)
        return Response({'content': markdown_content})


class PlainView(BaseContentView):
    def handle_content(self, content: str, request: Request):
        return Response({'content': content})


class GPTView(BaseContentView):
    def handle_content(self, content: str, request: Request):
        content = MarkdownConverterX().convert(content)

        openai_api_key = parse_api_key_from_headers(request.headers, key_name='X-OPENAI-API-KEY')

        if not openai_api_key:
            return Response({'error': "Missing OpenAI API key."}, status=status.HTTP_400_BAD_REQUEST)

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant tasked with providing a structured one-page summary with links.",
            },
            {
                "role": "user",
                "content": content,
            }
        ]

        try:
            response = OpenAI(api_key=openai_api_key).chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            choice = response.choices[0]
            summary = choice.message.content
            finish_reason = choice.finish_reason

            # Optionally, log or handle different finish_reasons
            if finish_reason == 'stop':
                # This is the ideal scenario where a complete message is returned
                pass  # You can implement logging or additional handling here
            elif finish_reason in ['length', 'function_call', 'content_filter']:
                # Handle these scenarios according to your application's needs
                pass
            elif finish_reason == 'null':
                # Consider how to handle incomplete responses
                pass

            return Response({'content': summary, 'finish_reason': finish_reason})
        except Exception as e:
            data = {'error': f"Failed to generate summary: {str(e)}"}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
