import os

import openai

openai.api_key = os.environ.get('OPEN_API_KEY')


# Define the generate_text function
def generate_text(prompt, max_tokens=100):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{prompt}"}],
            max_tokens=max_tokens
        )
        return response.choices[0].message["content"]
    except Exception as error:
        print(error)


def generate_cv_dict(data: dict) -> dict:

    personal_info = data.get('personal_info', {})

    # Work experience
    work_experience = data.get('work_experience', [])

    # Generate descriptions for work experience
    for experience in work_experience:
        if 'description' not in experience:
            prompt = f"Describe the responsibilities and achievements of a {experience['job_title']} at" \
                     f" {experience['company']} using {', '.join(experience['skills'])}."
            experience['description'] = generate_text(prompt)

    # Education
    education = data.get('education', [])

    # Skills
    skills = data.get('skills', [])

    # Projects or portfolio
    projects = data.get('projects', [])

    # Generate descriptions for projects
    for project in projects:
        if 'description' not in project:
            prompt = f"Describe a project using {', '.join(project['skills'])} with the goal of {project['goal']}."
            project['description'] = generate_text(prompt)

    # Other sections
    awards = data.get('awards', [])
    languages = data.get('languages', [])
    volunteer_work = data.get('volunteer_work', [])

    # Professional summary or objective
    prompt = f'base of this experience: {work_experience}, create some summary information for my cv'
    summary = generate_text(prompt, max_tokens=200)

    # Combine all information and format the CV
    cv = {
        'personal_info': personal_info,
        'summary': summary,
        'work_experience': work_experience,
        'education': education,
        'skills': skills,
        'projects': projects,
        'awards': awards,
        'languages': languages,
        'volunteer_work': volunteer_work
    }
    return cv
