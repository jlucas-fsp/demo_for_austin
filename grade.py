from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.rate_limiters import InMemoryRateLimiter
import json
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import StateGraph, END
from loguru import logger
import streamlit as st
from streamlit import session_state as ss
from typing_extensions import TypedDict
from utils import get_prompt, get_document
from dotenv import load_dotenv
from pprint import pprint
import os

#loading api keys from .env file
load_dotenv()

class State(TypedDict):
    # input to the graph
    question: str
    answer: str
    grading_criteria: str

    # generated from the graph
    grade: int # 0-100
    reason_for_grade: str

class Grade(BaseModel):
    '''
    Object containin the grade and reason for the grade of a piece of work from a student
    '''
    grade: int = Field(..., ge=0, le=100)
    reason_for_grade: str

def generate_grade(state: State):
    
    template = get_prompt("grade")
    chain = (
        ChatPromptTemplate.from_template(template)
        | ChatAnthropic(model='claude-3-haiku-20240307', temperature=0).with_structured_output(Grade)
    )
    res = chain.invoke({
        'question': state['question'],
        'answer': state['answer'],
        'grading_criteria': state['grading_criteria']
    })
    return {'grade': res.grade, 'reason_for_grade': res.reason_for_grade}

def construct_graph():
    graph = StateGraph(State)
    
    # Define nodes
    graph.add_node(generate_grade)

    # Define edges
    graph.set_entry_point('generate_grade')
    graph.add_edge('generate_grade', END)

    flow = graph.compile()
    return flow

if __name__ == "__main__":
    question = get_document("example_question")
    answers = [get_document(f"example_answer{i}") for i in range(1, 9)]
    grading_criteria = get_document("grading_criteria")

    if os.path.isfile('data/grades.json'):
        logger.info('Loading grades from file...')
        with open('data/grades.json', 'r') as f:
            res = json.load(f)
    else:
        logger.info('Grading answers...')

        inputs = [{
            'question': question,
            'answer': answer,
            'grading_criteria': grading_criteria
        } for answer in answers]

        flow = construct_graph()
        res = flow.batch(inputs)
        with open('data/grades.json', 'w') as f:
            json.dump(res, f, indent=4)
        logger.info('Grades generated and saved to file.')

    pprint(res)
    print(len(res))

    st.title('Grading Results:')
    st.subheader('Question:')
    st.write(question)
    st.subheader('Grading Criteria:')
    st.write(grading_criteria)

    for i,  entry in enumerate(res):
        st.subheader(f'Answer {i+1}:')
        st.write(entry['answer'])
        st.write(f'Grade: {entry["grade"]}')
        st.write(f'Reason for Grade:\n{entry["reason_for_grade"]}')
        st.write('---') 

