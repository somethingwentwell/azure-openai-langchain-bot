# azure-openai-langchain-bot

This is an API built with FastAPI that allows you to generate text using OpenAI's GPT-3 models, along with other NLP tools and utilities provided by the LangChain library.

## Prerequisites

To run this chatbot, you will need the following:

- Docker
- Docker Compose

## Installation

1. Clone this repository to your local machine.

2. Set up the environment variables in a `.env` file. You can copy the `.env.example` file and rename it to `.env`, then replace the placeholders with your own API key and bot token.

```
MicrosoftAppType=MultiTenant
MicrosoftAppId=
MicrosoftAppPassword=
MicrosoftAppTenantId=
OPENAI_API_TYPE=azure
OPENAI_API_VERSION=2022-12-01
OPENAI_API_BASE=
OPENAI_API_KEY=
COMPLETION_DEPLOYMENT_NAME=text-davinci-003
COMPLETION_MODEL_NAME=text-davinci-003
EMBEDDING_DEPLOYMENT_NAME=text-embedding-ada-002
CHAT_DEPLOYMENT_NAME=gpt-35-turbo
CHAT_MODEL_NAME=gpt-35-turbo
CHAT_SYSTEM_PROMPT=You are an GitLab AI assistant that helps people find information. You must use the given tools to answer questions. 
TOOLS_CATEGORY=GitLab Docs
ZAPIER_NLA_API_KEY=
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
LC_API_URL=http://host.docker.internal/run
```

Make sure to keep the `.env` file private and do not commit it to version control.

3. Docker-compose with latest image:
```
docker-compose -f docker-compose-db.yml up
docker-compose up
```
or
```
python -m uvicorn main:app --reload --port 8000
```

4. Test the API:
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