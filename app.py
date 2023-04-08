from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]

history = []


@app.route("/")
def home():
    return render_template("index.html", history=history)


@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]
    prompt = f"User: {message}\nAI:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    reply = response.choices[0].text.strip()
    history.append((message, reply))
    return {"message": reply}


app.run(debug=True)