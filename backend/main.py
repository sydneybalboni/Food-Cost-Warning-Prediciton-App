from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os
from prometheus_flask_exporter import PrometheusMetrics
import boto3
import csv

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)

# Load .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the API key

chat_history = []

# Initialize S3 client
s3 = boto3.client('s3')

def load_food_price_warnings_from_s3(country):
    try:
        response = s3.get_object(Bucket='food-cost-chat-app', Key='food_price_warnings.csv')
        data = response['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(data)
        for row in reader:
            if row['Country'] == country:
                return row['Severity']
        return "No data available for this country."
    except Exception as e:
        print("Error loading food price warnings from S3:", e)
        return "Error occurred while retrieving data."

@app.route('/api/send-message', methods=['POST'])
@metrics.summary('request_latency_seconds', 'Request Latency')
def send_message():
    if request.method == 'POST':
        data = request.json
        user_message = data.get('message')
        nation = data.get('nation')
        language = data.get('language')

        if not user_message or not nation or not language:
            abort(400, description='Missing required data in request.')

        # Determine food price warning severity for the given country
        warning = load_food_price_warnings_from_s3(nation)

        conversation_prompt = f"""
        Your conversation prompt...
        """

        messages = [
            {"role": "user", "content": "OUR PREVIOUS CHAT HISTORY: " + str(chat_history)},
            {"role": "system", "content": conversation_prompt},
            {"role": "user", "content": user_message}
        ]

        try:
            bot_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            ).choices[0].message['content']
        except Exception as e:
            abort(500, description=str(e))

        chat_history.append("USER QUESTION: " + user_message)
        chat_history.append("YOUR RESPONSE: " + bot_response)

        return jsonify({"reply": bot_response, "food_price_warning": warning}), 200

if __name__ == '__main__':
    app.run(debug=True)
