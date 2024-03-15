# ChatGPT Custom Action Server for Web Crawling

## Overview

This project implements a custom action server for ChatGPT, designed to enhance its capabilities with real-time web crawling functionalities. By integrating this server, ChatGPT can fetch and process web content on demand, enabling it to provide up-to-date information and perform dynamic content analysis.

## Features

- **Real-Time Web Crawling**: Fetch web content in real-time as requested by ChatGPT.
- **Content Processing**: Analyze and preprocess web content to fit ChatGPT's response format.
- **Secure API Key Access**: Restrict access through secure API key authentication.
- **Customizable Crawling Parameters**: Configure crawling behavior per request.

## Quick Start

1. **Clone the Repository**
   ```
   git clone <repository-url> . 
   ```
2. **Set Environment Variables**
   Create a `.env` file based on the provided `.env.example` and fill in your environment-specific values.
3. **Build and Run with Docker Compose**
   ```
   docker-compose -f docker-compose.dev.yml up --build
   ```
4. **Accessing the Server**
   The server will be available at `http://localhost:8000` (or a custom port defined in `.env`).

## Configuration (.env)

- **`DJANGO_DEBUG`**: Set to '0' in production.
- **`DJANGO_SECRET`**: Set this to a secure, unique value for your instance.
- **`DJANGO_ALLOWED_HOSTS`**: Hosts from which the server can be accessed (comma separated), e.g., "127.0.0.1".
- **`CRAWLER_API_KEY`**: Define an API key for authenticating crawling requests.
- **`OPENAI_API_KEY`**: Define an API key for authenticating OpenAI requests.

## API Key Authentication

Due to custom GPT limitations accepting only one secret header, we require a single `X-API-KEYS` header packing all necessary keys in JSON:

- **Keys**:
  - `X-CRAWLER-API-KEY`: Access to web crawling.
  - `X-OPENAI-API-KEY`: Needed for GPT processing.

- **Format**:
  ```plaintext
  X-API-KEYS: {"X-CRAWLER-API-KEY": "your_key", "X-OPENAI-API-KEY": "your_key"}
  ```

- **Example**:
  ```bash
  curl -X POST "https://crawler-your-domain.com/api/view/md/" \
       -H "Content-Type: application/json" \
       -H "X-API-KEYS: {\"X-CRAWLER-API-KEY\": \"your_key\", \"X-OPENAI-API-KEY\": \"your_key\"}" \
       -d '{"url": "https://example.com"}'
  ```

Replace `your_key` with actual API keys. Ensure key confidentiality.

## Service Endpoints

The service provides three main endpoints, each designed for specific functionalities within our web crawling and content processing platform. All endpoints require authentication via headers to ensure secure access.
The OpenAPI specs to be used in custom GPT actions can be found in [this gist](https://gist.github.com/numpde/23311ceacb35feefd0103226a693e1e8).

#### General Authentication

- **Required for All Requests**: Each request must include the `X-API-KEYS` header containing the `X-CRAWLER-API-KEY`.
- **Format**: `X-API-KEYS: {"X-CRAWLER-API-KEY": "your_crawler_api_key"}`

#### Endpoints Overview

1. **Markdown Conversion**
   - **Path**: `/api/view/md/`
   - **Method**: `POST`
   - **Description**: Converts fetched web content to Markdown format.
   - **Payload**: `{ "url": "https://example.com" }`
   - **Authentication**: `X-CRAWLER-API-KEY` required.

2. **GPT-Processed Markdown Conversion**
   - **Path**: `/api/view/md/gpt/`
   - **Method**: `POST`
   - **Description**: Processes fetched content through the GPT model and converts it to Markdown.
   - **Payload**: `{ "url": "https://example.com" }`
   - **Authentication**: Requires both `X-CRAWLER-API-KEY` and `X-OPENAI-API-KEY` packed into the `X-API-KEYS` header.
   - **Header Example**: `X-API-KEYS: {"X-CRAWLER-API-KEY": "your_crawler_api_key", "X-OPENAI-API-KEY": "sk-your_openai_api_key"}`

3. **Plain Content Fetch**
   - **Path**: `/api/view/plain/`
   - **Method**: `POST`
   - **Description**: Fetches web content and returns it as plain text.
   - **Payload**: `{ "url": "https://example.com" }`
   - **Authentication**: `X-CRAWLER-API-KEY` required.

#### CURL Example for GPT-Processed Markdown Conversion

```bash
curl -X POST "https://crawler-your-domain.com/api/view/md/gpt/" \
     -H "Content-Type: application/json" \
     -H "X-API-KEYS: {\"X-CRAWLER-API-KEY\": \"your_crawler_api_key\", \"X-OPENAI-API-KEY\": \"sk-your_openai_api_key\"}" \
     -d '{"url": "https://example.com"}'
```

Replace `your_crawler_api_key` and `sk-your_openai_api_key` with your actual API keys. Ensure the confidentiality of your API keys to prevent unauthorized use.

## Contributing

We welcome contributions and suggestions! Please create a pull request or issue for any feature requests, bug reports, or improvements.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
