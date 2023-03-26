# views.py
import ast
import os
import re

import openai
from flask import request, redirect, url_for, Blueprint, session, jsonify, render_template, make_response

from cv_generator import generate_cv_dict
from pdf_generator import generate_pdf_doc

views_blueprint = Blueprint('views', __name__)

# Set your OpenAI API key
openai.api_key = os.environ.get('OPEN_API_KEY')


def generate_text(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{prompt}"}]
        )
        return response.choices[0].message["content"]
    except Exception as error:
        print(error)


@views_blueprint.route('/job-title', methods=['POST'])
def process_job_title():
    job_title = request.form['job_title']

    prompt = f"Enumerate the skills and technologies for a {job_title} without explanations."
    key_knowledge = generate_text(prompt)

    # Split the text into a list of skills using regex
    skills = re.split(r'\d+\.', key_knowledge.strip())

    # Remove any empty strings from the list
    skills = [skill.strip() for skill in skills if skill.strip()]

    # store all skills in session to be able to use it later in templates
    session['skills'] = skills

    return redirect(url_for('personal'))


@views_blueprint.route('/personal-info', methods=['POST'])
def process_personal_info():
    personal_info = {
        "full_name": request.form["full_name"],
        "phone": request.form["phone"],
        "email": request.form["email"],
        "linkedin": request.form["linkedin"]
    }

    session['cv'] = {"personal_info": personal_info}
    return redirect(url_for('work'))


@views_blueprint.route('/work-experience', methods=['POST'])
def process_work_experience():
    work_experience = request.get_json()
    if work_experience:
        session['cv']['work_experience'] = work_experience
        session.modified = True
    return jsonify(success=True)


@views_blueprint.route('/education-experience', methods=['POST'])
def process_education_experience():
    education_experience = request.get_json()
    if education_experience:
        session['cv']['education'] = education_experience
        session.modified = True
    return jsonify(success=True)


@views_blueprint.route('/projects-experience', methods=['POST'])
def process_project_experience():
    projects_experience = request.get_json()
    if projects_experience:
        session['cv']['projects'] = projects_experience
        session.modified = True
    return jsonify(success=True)


@views_blueprint.route('/addition-info', methods=['POST'])
def process_addition_info():
    awards = request.form["awards"]
    languages = request.form["languages"]
    skills = request.form["skills"]

    if awards:
        session['cv']['awards'] = [awards]
    if languages:
        session['cv']['languages'] = [languages]
    if skills:
        session['cv']['skills'] = [skills]

    cv = generate_cv_dict(session['cv'])
    return render_template('cv.html', cv=cv)


@views_blueprint.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    personal_info = {
        "full_name": request.form["full_name"],
        "phone": request.form["phone"],
        "email": request.form["email"],
        "linkedin": request.form["linkedin"]
    }
    summary = request.form["summary"]

    jobs_count = 0
    for key in request.form.keys():
        if key.startswith("job_title"):
            jobs_count += 1

    education_count = 0
    for key in request.form.keys():
        if key.startswith("institution"):
            education_count += 1

    projects_count = 0
    for key in request.form.keys():
        if key.startswith("project_title"):
            projects_count += 1

    projects = []
    for number in range(projects_count):
        project = {
            "title": request.form[f"project_title_{number}"],
            "goal": request.form[f"goal_{number}"],
            "description": request.form[f"project_description_{number}"],
            "skills": ast.literal_eval(request.form[f"project_skills_{number}"]),
        }
        projects.append(project)

    educations = []
    for number in range(education_count):
        education = {
            "place": request.form[f"place_{number}"],
            "institution": request.form[f"institution_{number}"],
            "degree": request.form[f"degree_{number}"],
            "year": request.form[f"year_{number}"],
        }
        educations.append(education)

    works = []
    for number in range(jobs_count):
        work = {
            "job_title": request.form[f"job_title_{number}"],
            "start_date": request.form[f"start_date_{number}"],
            "end_date": request.form[f"end_date_{number}"],
            "company": request.form[f"company_{number}"],
            "description": request.form[f"description_{number}"],
            "skills": ast.literal_eval(request.form[f"work_skills_{number}"]),
        }
        works.append(work)

    skills, languages, awards = [], [], []
    if request.form.get("skills"):
        skills = ast.literal_eval(request.form.get("skills"))
    if request.form.get("languages"):
        languages = ast.literal_eval(request.form.get("languages"))
    if request.form.get("awards"):
        awards = ast.literal_eval(request.form.get("awards"))

    final_cv = {
        'personal_info': personal_info,
        'summary': summary,
        'work_experience': works,
        'education': educations,
        'skills': skills,
        'projects': projects,
        'awards': awards,
        'languages': languages,
    }
    pdf_data = generate_pdf_doc(final_cv)

    # Create a response with the PDF file as attachment
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=cv.pdf'

    return response
