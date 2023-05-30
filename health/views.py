"""
Health Views

This file defines a Flask blueprint for handling the health page for displaying
health explanations, tips, and facts, also providing the function to display
random conditions from a CSV file.
"""


from flask import Blueprint, render_template, request, redirect, url_for
import csv
import os
import random
import re
from collections import OrderedDict


health_blueprint = Blueprint('health', __name__, template_folder='templates/features')


@health_blueprint.route('/health', methods=['GET', 'POST'])
def health():
    """
    Handles the health route for displaying disease information and symptoms.

    Returns:
        string: The rendered HTML template with disease information.

    Notes:
        - If the request method is 'POST', redirects back to the health route.
        - Randomly selects four diseases from the CSV file and retrieves their information.
        - Disease information is processed and stored in a list.
        - The list of disease information is passed to the 'features/health.html' template for rendering.
    """
    if request.method == 'POST':
        return redirect(url_for('health'))

    all_disease = []
    random_list = random.sample(read_csv_columns(os.path.dirname(__file__) + "/disease.csv", 1), 4)
    dict_ = sym_dict_(os.path.dirname(__file__) + "/disease.csv")

    for disease in random_list:
        d_list = []
        sym = (get_symptoms_from_data(disease))
        sym_convert(sym, dict_)
        d_list.extend((get_name(disease), split_data_decs(disease), OrderedDict.fromkeys(sym)))
        all_disease.append(d_list)

    return render_template('features/health.html', result=all_disease)


def read_csv_columns(csv_file, column_number):
    """
    Read the specified columns from a CSV file.

    Args:
        csv_file (str): The path to the CSV file.
        column_number (int): The number of columns to read.

    Returns:
        list: A list of columns read from the CSV file.
    """
    columns = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            columns.append(row[:column_number])  # Add first three columns to the list
    return columns


def get_symptoms(data):
    """
    Extract symptoms from the data.

    Args:
        data (list): The data containing symptoms.

    Returns:
        list: A list of symptoms extracted from the data.
    """
    symptoms = []
    for item in data:
        if 'symptoms' in item:
            symptoms.append(item['symptoms'])
    return symptoms


def sym_dict_(csv_file):
    """
    Create a dictionary of symptoms.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        dict: A dictionary of symptoms.
    """
    dict_ = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line[1:-1]
            key, value = line[0:].split(",")[:2]
            dict_[key] = value
    return dict_


def split_data_decs(d):
    """
    Split the data description.

    Args:
        d (list): The data containing the description.

    Returns:
        str: The split data description.
    """
    element_parts = d[0].split("],", 1)
    return re.sub(r'[\s"]+', ' ', element_parts[1].strip())


def sym_convert(sym_list, dict_):
    """
    Convert symptom names using a dictionary.

    Args:
        sym_list (list): The list of symptoms to convert.
        dict_ (dict): The dictionary containing symptom conversions.
    """
    for i in range(len(sym_list)):
        if sym_list[i] in dict_:
            sym_list[i] = dict_[sym_list[i]]


def get_symptoms_from_data(data):
    """
    Extracts symptoms from the provided data.

    Args:
        data (list): A list containing the data.

    Returns:
        list: A list of symptoms extracted from the data.
    """
    start_index = data[0].index('[{')
    end_index = data[0].index('}]')
    parsed_data = eval(data[0][start_index:end_index + 2])

    symptoms_list = get_symptoms(parsed_data)

    return symptoms_list


def get_name(disease):
    """
    Retrieves the name of the disease from the provided disease data.

    Args:
        disease (list): A list containing the disease data.

    Returns:
        str: The name of the disease.
    """
    disease = disease[0]
    disease = disease.split(",")
    return disease[1]
