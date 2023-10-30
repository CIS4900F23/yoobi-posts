"""API route for the Q&A page"""

import os
import openai
from flask import request
from flask_restx import Namespace, Resource

api = Namespace('ask', description='Q&A page operations')

openai.api_key = os.getenv("OPENAI_API_KEY")

class Ask(Resource):   
    def get(self):
        args = request.args
        question = args["q"]
        qString= f'''
        You are a website devoted to providing information about the topic of \"universal basic income\". 
        You are to answer any questions a user may have about this topic, and only this topic.
        \n\nExamples:
        \nUser: What is universal basic income?
        \nYou: Universal basic income (UBI) is a social welfare proposal in which all citizens of a given population regularly receive a guaranteed income in the form of an unconditional transfer payment (i.e., without a means test or need to work).
        \n\nUser: Are Basic Income and Universal Basic income the same thing?
        \nYou: Yes, these are different ways of describing the same thing.
        \n\nUser: How are you?
        \nYou: I am good. I am here to answer any questions you may have about universal basic income.
        \n\nUser: What is Batman's secret identity?
        \nYou: I am here to answer any questions you may have about universal basic income.
        \nUser: Who is Lionel Messi?
        \n\nYou: I am sorry, I'm here to answer any questions you may have about universal basic income.
        \n\nCurrent conversation:
        \nUser: {question}
        \nYou: \n
        '''
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=qString,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0  
            )

        return response

api.add_resource(Ask, "")