from schema import CurriculoEstruturado


def build_structured_string(data : CurriculoEstruturado):
    print("Dados do curriculo: ", data)


def  structured_cv_to_string(data : dict) -> str:

    if not isinstance(data, dict):
        raise Exception ("O curriculo do estruturado deve ser uma intância pydantic da '")

    build_structured_string(data)