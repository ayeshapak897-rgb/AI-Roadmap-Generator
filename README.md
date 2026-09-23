````markdown
# 🗺️ AI Roadmap Generator

An AI-powered personalized learning roadmap generator.

## Tech Stack

- Python
- Streamlit
- Groq API
- OpenAI GPT-OSS 120B

## Features

- Learning domain selection
- Beginner / Intermediate / Advanced levels
- Weekly study hours
- Learning duration
- Personalized learning goal
- AI-generated weekly roadmap
- Practical tasks
- Projects
- Checkpoints
- Final capstone
- Markdown download

## Deployment

The application is designed for Streamlit Community Cloud.

No local installation is required.

## Required Secret

Add this in Streamlit Cloud Secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"
````

Never commit your API key to GitHub.

## Model

The application uses:

```text
openai/gpt-oss-120b
```

through the Groq API.

```
```
