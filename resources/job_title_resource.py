import re

import openai
from flask_restful import Resource
from flask import request


# Set your OpenAI API key
openai.api_key = "sk-"


# Define the generate_text function
def generate_text(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{prompt}"}]
        )
        return response.choices[0].message["content"]
    except Exception as error:
        print(error)


class JobTitleResource(Resource):

    def post(self):
        job_title = request.json['job_title']
        prompt = f"Enumerate the key skills and technologies for a {job_title} without explanations."
        key_knowledge = generate_text(prompt)

        # Split the text into a list of skills using regex
        skills = re.split(r'\d+\.', key_knowledge.strip())

        # Remove any empty strings from the list
        skills = [skill.strip() for skill in skills if skill.strip()]

        # Create a dictionary with numbers as keys and skills as values
        skills_dict = {i + 1: skill for i, skill in enumerate(skills)}

        return {'key_knowledge': skills_dict}
