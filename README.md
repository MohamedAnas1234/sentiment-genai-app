# AI-Powered Sentiment Analysis with Groq

**DockerHub Image:** [https://hub.docker.com/r/anasnasu26/sentiment-genai-app](https://hub.docker.com/r/anasnasu26/sentiment-genai-app)

This repository builds upon the concept of Sentiment Analysis using Hugging Face Transformers and infuses it with Generative AI via the Groq LLM API. The application is served using a Flask REST API and is containerized using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed.
- A [Groq API Key](https://console.groq.com/).
- Git installed.

## Running Locally (Without Docker)

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set the Groq API Key**:
   - Windows (PowerShell): `$env:GROQ_API_KEY="your_api_key_here"`
   - Linux/Mac: `export GROQ_API_KEY="your_api_key_here"`

3. **Run the Flask App**:
   ```bash
   python app.py
   ```

4. **Test the Endpoint**:
   ```bash
   curl -X POST http://localhost:5000/analyze \
        -H "Content-Type: application/json" \
        -d '{"text":"I have been feeling very anxious lately."}'
   ```

## Containerization & DockerHub

A shell script `build_and_push.sh` is provided to easily build the Docker image and push it to your DockerHub repository.

1. Make the script executable (Linux/Mac/WSL):
   ```bash
   chmod +x build_and_push.sh
   ```
2. Login to DockerHub:
   ```bash
   docker login
   ```
3. Run the script:
   ```bash
   ./build_and_push.sh
   ```

To run the container locally:
```bash
docker run -p 5000:5000 -e GROQ_API_KEY="your_api_key_here" anasnasu26/sentiment-genai-app:latest
```

## Version Control (Git & GitHub)

To push this application to GitHub, follow these git commands:

1. **Initialize the local repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Flask app with Hugging Face and Groq"
   ```

2. **Create a repository on GitHub**.

3. **Link your local repository to GitHub** (Replace `<your-username>` and `<repo-name>`):
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
