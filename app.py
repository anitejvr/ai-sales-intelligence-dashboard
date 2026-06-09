from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os
import json 

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        transcript = request.form["transcript"]

        prompt = f"""
        Analyze this sales transcript.

        Return ONLY valid JSON in this format:

        {{
            "summary": "",
            "deal_risk": "",
            "probability_to_close": 0,
            "objections": [],
            "action_items": [],
            "follow_up_email": ""
        }}

        deal_risk should be one of:
        - Low
        - Medium
        - High

        probability_to_close should be an integer from 0 to 100.

        Transcript:

        {transcript}
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        raw_response = response.choices[0].message.content

        print("RAW RESPONSE:")
        print(raw_response)

        result = json.loads(raw_response)

    return render_template(
        "index.html",
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)