from services.openai_service import client



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

def gen_embedding_from_text(cv_content : str):

    try:

        response = client.embeddings.create(
            model='text-embedding-3-small',
            input=cv_content,
        )
        return response.data[0].embedding
        
    except Exception as e:
        print("Houve um erro na comunicação com a openAI: ", str(e))
        raise
