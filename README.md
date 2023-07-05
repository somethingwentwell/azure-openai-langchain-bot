# azure-openai-langchain-bot

This is an API built with FastAPI that allows you to generate text using OpenAI's GPT-3 models, along with other NLP tools and utilities provided by the LangChain library.

## Prerequisites

To run this chatbot, you will need the following:

- Docker
- Docker Compose

## Installation

1. Clone this repository to your local machine.

2. Build the Docker image:

```
docker buildx build --platform linux/amd64 --no-cache  -t langchain-base-image .
```

3. Set up the environment variables in a `.env` file. You can copy the `.env.example` file and rename it to `.env`, then replace the placeholders with your own API key and bot token.

```
AGENT_TYPE=
OPENAI_API_TYPE=azure
OPENAI_API_VERSION=2023-03-15-preview
OPENAI_API_BASE=
OPENAI_API_KEY=
EMBEDDING_DEPLOYMENT_NAME=text-embedding-ada-002
CHAT_DEPLOYMENT_NAME=gpt-35-turbo-16k
CHAT_MODEL_NAME=gpt-35-turbo-16k
CHAT_SYSTEM_PROMPT=You are an AI Shopping Helper that helps people to find mall information.
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
MicrosoftAppType=MultiTenant
MicrosoftAppId=
MicrosoftAppPassword=
MicrosoftAppTenantId=
LC_API_URL=http://host.docker.internal/run
ZAPIER_NLA_API_KEY=
BING_SUBSCRIPTION_KEY=
BING_SEARCH_URL=https://api.bing.microsoft.com/v7.0/search/
AZURE_COGNITIVE_SEARCH_URL=
AZURE_COGNITIVE_SEARCH_KEY=
AZURE_COGNITIVE_SEARCH_INDEX_NAME=
AZURE_COGNITIVE_SEARCH_DESC=
AZURE_COGS_KEY=
AZURE_COGS_ENDPOINT=
AZURE_COGS_REGION=
TOTAL_TOKEN_LIMIT=
TOTAL_TOKEN_LIMIT_PER_USER=

```

Make sure to keep the `.env` file private and do not commit it to version control.

4. Docker-compose with latest image:
```
docker-compose -f docker-compose-db.yml up
docker-compose up
```
or
```
python -m uvicorn main:app --reload --port 8000
```

5. Test the API:
```
curl --location --request POST 'http://127.0.0.1:80/run' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "Hi",
    "id": "testid01"
}'
```

## Admin API

Run the API
```
uvicorn adminapi:app --reload --port 8100
```

Swagger
```
http://localhost:8100/docs
```

## Contributing

If you'd like to contribute to this project, please open an issue or pull request on GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.