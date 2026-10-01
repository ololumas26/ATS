# app.py
# Ponto de entrada da API.
from fastapi import FastAPI

from routers.cv_router import router as cv_router
from routers.job_router import router as job_router


app = FastAPI(title='ATS - Applicant Tracking System')

app.include_router(cv_router)
app.include_router(job_router)
