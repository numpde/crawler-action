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

## Contributing

We welcome contributions and suggestions! Please create a pull request or issue for any feature requests, bug reports, or improvements.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
