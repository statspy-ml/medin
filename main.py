import json
import time
import random
import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Form, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from topics import TOPICS_LIST
from principios_ativos import PRINCIPIO


MAX_RETRIES = 5
BACKOFF_FACTOR = 0.5
TEMPERATURE = 0.0
MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-4-0613"

load_dotenv(".env")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/classify/")
async def classify_text(request: Request, text: str = Form(...)):
    paragraph = text

    functions_topics = [{
        "name": "print_topics",
        "description": "A function that prints the given medicament therapeutic classification ",
        "parameters": {
            "type": "object",
            "properties": {
                "topics": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": TOPICS_LIST
                    },
                    "description": "The Topics",
                },
            },
            "required": ["topics"],
        }}]

    results = []

    messages = [{"role": "user", "content": paragraph}]
    paragraph_result = {"paragraph": paragraph, "sentence":paragraph}
    
    function_call = {"name": "print_topics"}
    for attempt in range(MAX_RETRIES):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=messages,
                functions=functions_topics,
                function_call=function_call,
                temperature=TEMPERATURE
            )
            function_call_response = response.choices[0].message["function_call"]
            argument = json.loads(function_call_response["arguments"])
            paragraph_result["topics"] = argument
            break
        except openai.api_errors.TimeoutError as e:
            if attempt == MAX_RETRIES - 1:
                raise e

            sleep_time = BACKOFF_FACTOR * (2 ** attempt) + random.random()
            time.sleep(sleep_time)

    results.append(paragraph_result)
    # Before sending to template
    if isinstance(paragraph_result["topics"].get('topics', ''), str):
        paragraph_result["topics"]['topics'] = [paragraph_result["topics"].get('topics', '')]


    return templates.TemplateResponse("index.html", {"request": request, "results": results})




