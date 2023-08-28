import openai
import json
import time
import random
import os
import sqlite3 
from dotenv import load_dotenv

from topics_pt import TOPICS_LIST

load_dotenv(".env")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

MAX_RETRIES = 5
BACKOFF_FACTOR = 0.5
TEMPERATURE = 0.0
MODEL = "gpt-4-0613"

class MedicationClassifier:
    
    def __init__(self):

        self.conn = sqlite3.connect('medications.db')  
        self.cursor = self.conn.cursor()


        self.functions_topics = [{
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

    def classify_text(self, text):
        messages = [{"role": "user", "content": text}]
        paragraph_result = {"paragraph": text, "sentence": text}
        function_call = {"name": "print_topics"}
        
        for attempt in range(MAX_RETRIES):
            try:
                response = openai.ChatCompletion.create(
                    model=MODEL,
                    messages=messages,
                    functions=self.functions_topics,
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

        if isinstance(paragraph_result["topics"].get('topics', ''), str):
            paragraph_result["topics"]['topics'] = [paragraph_result["topics"].get('topics', '')]

        return paragraph_result

    def get_medications_by_type(self, medicament_type):
        self.cursor.execute('SELECT name FROM medications WHERE medicament_type=?', (medicament_type,))
        return [item[0] for item in self.cursor.fetchall()]

    def close(self):
        self.conn.close()

