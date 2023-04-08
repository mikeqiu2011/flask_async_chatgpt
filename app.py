from flask import Flask, render_template, request
import openai
import os
import asyncio
import concurrent.futures

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]

executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

history = []

def chat_wrapper(message):
    prompt = {'role': 'user',
              'content': message}
    history.append(prompt)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=history
    )

    reply = response.choices[0].message.content
    history.append({'role': 'assistant',
                    'content': reply})

    return {"message": reply}

async def async_chat(message):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(executor, chat_wrapper, message)
    return response



@app.route("/")
def home():
    return render_template("index.html", history=history)


@app.route("/chat", methods=["POST"])
async def chat():
    message = request.json["message"]

    result = await async_chat(message)
    # result = chat_wrapper(message)
    return result



app.run(debug=True)