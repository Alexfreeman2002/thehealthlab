"""
Quiz Views

This file defines a Flask blueprint for handling the Quiz page for retrieving
questions and rendering the quiz.
"""


import json

from flask import Blueprint, render_template
from app import app
from models import Question
import random
from Quiz.forms import QuizForm

quiz_blueprint = Blueprint('Quiz', __name__, template_folder='templates/features')


@quiz_blueprint.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
    Renders the quiz template and handles form submission.

    Returns:
        Rendered template 'features/quiz.html' with form and questions data.
    """
    form = QuizForm()

    if form.validate_on_submit():
        num_questions = int(form.number_of_questions.data)
        questions = retrieve_random_questions(num_questions)

        return render_template('features/quiz.html',
                               form=form,
                               questions=questions,
                               questions_json=json.dumps(questions))

    return render_template('features/quiz.html', form=form)


def retrieve_questions():
    """
    Retrieves all questions from the database.

    Returns:
        List of all questions.
    """
    with app.app_context():
        return Question.query.all()


def retrieve_random_questions(num_questions):
    """
    Retrieves a random selection of questions from the database.

    Args:
        num_questions: Number of questions to retrieve.

    Returns:
        List of formatted random questions.
    """
    all_questions = retrieve_questions()
    random_questions = random.sample(all_questions, num_questions)
    formatted_questions = []

    for question in random_questions:
        formatted_question = {
            'text': question.question,
            'choices': [question.answer_one,
                        question.answer_two,
                        question.answer_three,
                        question.answer_four],
            'correct_answer': question.correct_answer
        }
        formatted_questions.append(formatted_question)

    return formatted_questions


