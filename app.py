from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Define your API key and endpoint
API_KEY = "AIzaSyDZR6__W9vQ0utqMVLHTJWbiPF8ixEeDio"  # Replace with your actual API key
MODEL_ID = "gemini-1.5-flash-latest"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form['user_input']
    
    # Prepare the data to be sent in the request
    data = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }

    # Set headers for the request
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request to the Gemini API
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON and extract text
        response_data = response.json()
        generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
        return render_template('result.html', summary=generated_text)
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/summarize', methods=['POST'])
def summarize():
    user_input = request.form['long_user_input']
    
    # Prepare a specific prompt for summarizing long text
    prompt = f"Please summarize the following text in 50-100 words:\n\n{user_input}"

    # Prepare the data to be sent in the request
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    # Set headers for the request
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request to the Gemini API
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON and extract text
        response_data = response.json()
        generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
        return render_template('result.html', summary=generated_text)
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == '__main__':
    app.run(debug=True)