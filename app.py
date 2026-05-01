import os
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from groq import Groq

app = Flask(__name__)

# Initialize the Hugging Face sentiment analysis pipeline
# It will download the default model (distilbert-base-uncased-finetuned-sst-2-english) on first run
print("Loading Hugging Face sentiment model...")
# Explicitly specifying the model to avoid production warnings
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
print("Model loaded successfully.")

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """
    Expects a JSON payload: {"text": "The text to analyze", "api_key": "optional_groq_key"}
    Returns the sentiment and a generated response from Groq.
    """
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    user_text = data['text']
    api_key = os.environ.get("GROQ_API_KEY")
    
    # 1. Perform Sentiment Analysis using Hugging Face
    try:
        sentiment_result = sentiment_pipeline(user_text)[0]
        label = sentiment_result['label']
        score = sentiment_result['score']
    except Exception as e:
        return jsonify({"error": f"Sentiment analysis failed: {str(e)}"}), 500

    # 2. Generate a response using Groq LLM based on the sentiment
    if not api_key or api_key == "test_key":
        ai_response = "Could not generate AI response: Please set a valid GROQ_API_KEY environment variable."
    else:
        try:
            # Initialize Groq client with the provided key
            groq_client = Groq(api_key=api_key)
            
            # We use llama3-8b-8192 as a fast default model on Groq
            prompt = (
                f"A user said: \"{user_text}\". "
                f"The detected sentiment is {label} (confidence: {score:.2f}). "
                f"Provide a brief, empathetic, and helpful response addressing the user."
            )
            
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful, empathetic assistant in a healthcare/mental-health app."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant",
                max_tokens=150
            )
            
            ai_response = chat_completion.choices[0].message.content
        except Exception as e:
            ai_response = f"Could not generate AI response. Make sure your GROQ_API_KEY is valid. Error: {str(e)}"

    # 3. Return the combined result
    return jsonify({
        "original_text": user_text,
        "sentiment": {
            "label": label,
            "score": score
        },
        "ai_response": ai_response
    })

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Run the Flask app on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
