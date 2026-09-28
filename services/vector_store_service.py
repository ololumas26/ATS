

# {'candidate_name': 'ELISEU FRANCO SAMULOLO',
#   'email': 'eliseufranco26@hotmail.com',
#   'phone_number': '922 245 834',
#   'candidate_location': 'Angola',
#   'technical_skills': ['Python', 'JavaScript', 'C#', 'SQL', 'React', 'FastAPI', 'Flask', 'Vue.js', 'Tailwind CSS', 'Pandas', 'Matplotlib', 'HTML/CSS', 'PostgreSQL', 'Supabase', 'SQL Server', 'Docker', 'GitHub', 'REST APIs', 'Agile/Scrum'],
#   'total_experience_years': 3,
# 'profile_resume': "Results-driven Software Engineer with a Bachelor's degree in Management and Informatics and hands-on experience delivering scalable web applications end-to-end. Proficient in Python, JavaScript, React, FastAPI, and Flask, skilled in building user-focused products that create measurable impact."}



def build_embedding_text(data : dict):
    return f"""
    location: {data.get('candidate_location')},
    expirience: {data.get('total_experience_years')},
    profile: {data.get('profile_resume')},
    skills: {data.get('technical_skills')},
    """


def  structured_cv_to_string(data : dict) -> str:

    if not isinstance(data, dict):
        raise Exception ("O curriculo do estruturado deve ser uma intância pydantic da '")

    return build_embedding_text(data)