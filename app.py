# app.py
# Ponto de entrada da API.
from fastapi import FastAPI

from routers.analysis_router import router as analysis_router


app = FastAPI(title='ATS - Applicant Tracking System')

app.include_router(analysis_router)
