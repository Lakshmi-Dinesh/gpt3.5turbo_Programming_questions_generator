"""
@author:Lakshmi Dinesh
This class deals with the communication with the OpenAI GPT 3.5 turbo engine
"""

import json
import os
import traceback
import openai
from program_generator_constants import ENGINE, JSON_LOG_FILE, DEBUG_CONSOLE_LOG
from program_generator_utils import save_to_file, create_log_dir, wrap_content, show_message


class ProgramGeneratorEngine:
    def __init__(self):
        self.response = None
        self.q_nos = None
        self.file_path = None
        self.req_log = None
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.engine = ENGINE

    def train_engine(self):
        training_prompts = [
            {"role": "system", "content": "Lets learn to code in Java and Python programming languages."},
            {"role": "user", "content": "Generate 1 Beginner level programming question(s) in Python Tuples"},
            {"role": "assistant", "content": "Write a Python program that creates a tuple of your favorite fruits and "
                                             "prints out each fruit in the tuple using a for loop."},
            {"role": "user", "content": "Generate 1 Beginner level programming question(s) in Python Strings"}

        ]
        params = {'model': self.engine,
                  'messages': training_prompts,
                  'temperature': 0.6,
                  'max_tokens': 200
                  }
        try:
            training_response = openai.ChatCompletion.create(**params)
            if DEBUG_CONSOLE_LOG:
                print(training_response)
            process_finish_reason(training_response.choices[0]['finish_reason'])
            return True
        except openai.error.OpenAIError as error:
            print(f"OpenAI Error: {error}")
            return False
        except Exception as error:
            print(f"Unknown error sending initial openAI training data: {error}")
            traceback.print_exc()
            return False

    def set_gpt_params(self, file_path, q_nos, req_log):
        self.file_path = file_path
        self.q_nos = q_nos
        self.req_log = req_log

    def get_max_tokens(self):
        return min((self.q_nos + 1) * 50, 500)

    def generate_questions(self, prompt):
        tokens = self.get_max_tokens()
        params = {'model': self.engine,
                  'messages': [{"role": "user",
                                "content": prompt}],
                  'temperature': 0.6,
                  'max_tokens': tokens
                  }
        try:
            self.response = openai.ChatCompletion.create(**params)
        except openai.error.OpenAIError as error:
            print(f"OpenAI Error: {error}")
            return False
        except Exception as error:
            print(f"Error sending OpenAI request: {error}")
            traceback.print_exc()

        if not self.response:
            print("GPT None response")
            return False

        try:
            self.parse_json_log()
        except Exception as error:
            print(f"Error parsing json response: {error}")
            traceback.print_exc()

        process_finish_reason(self.response.choices[0]['finish_reason'])
        questions = self.response.choices[0]['message']['content']

        return save_to_file(self.file_path, wrap_content(questions))

    def parse_json_log(self):
        create_log_dir()
        json_log = json.dumps(json.loads(str(self.response)), indent=4)
        req_log = wrap_content(self.req_log)
        out_file_path = "Destination file: {}".format(self.file_path)
        try:
            with open(JSON_LOG_FILE, 'a+') as fObj:
                fObj.write("{}\n{}\n{}\n\n".format(req_log, json_log, out_file_path))
        except FileNotFoundError:
            print("Response log file not found")
        except Exception as error:
            print(f"Response log file Error: {error}")
            traceback.print_exc()


def process_finish_reason(reason):
    if reason == 'length':
        print("Response possibly truncated due to max token limit")
        show_message("Warning", "Response possibly truncated due to max token limit")
    elif reason == 'content_filter':
        print("Response omitted due to content flag")
        show_message("Warning", "Response omitted due to content flag")
    elif reason == 'null':
        print("API response still in progress")
        show_message("Warning", "API response still in progress")
    else:
        return
