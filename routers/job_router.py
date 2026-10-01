# routers/job_router.py
# Endpoints relacionados com vagas.
from fastapi import APIRouter

from schemas.job_schema import DescricaoVagaRequest


router = APIRouter(prefix='/job', tags=['job'])


@router.post('/description')
def receive_job_description(job: DescricaoVagaRequest):

    return {'job_description': job.job_description}
