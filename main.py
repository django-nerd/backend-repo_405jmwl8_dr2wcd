from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

from schemas import Lead, Application, TestResponse
from database import create_document, get_db, get_documents

app = FastAPI(title="TechConnect Systems GmbH API", version="1.0.0")

# CORS setup for frontend local/dev
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TechConnect API running"}

@app.get("/test", response_model=TestResponse)
async def test():
    db = await get_db()
    collections = await db.list_collection_names()
    return TestResponse(
        backend="FastAPI",
        database="MongoDB",
        database_url=os.getenv("DATABASE_URL", "mongodb://localhost:27017"),
        database_name=os.getenv("DATABASE_NAME", "appdb"),
        connection_status="connected",
        collections=collections,
    )

@app.post("/leads")
async def create_lead(lead: Lead):
    try:
        lead_id = await create_document("lead", lead.model_dump())
        return {"status": "ok", "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/applications")
async def create_application(apply: Application):
    try:
        app_id = await create_document("application", apply.model_dump())
        return {"status": "ok", "id": app_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/faqs")
async def get_faqs():
    # Example static FAQs; could be fetched from DB if needed
    faqs = [
        {"question": "How do you handle data security?", "answer": "We implement zero-trust architecture, end-to-end encryption, and regular audits."},
        {"question": "Do you offer on-prem options?", "answer": "Yes, all platforms can be deployed on-premise or as managed cloud."},
        {"question": "Where are you located?", "answer": "Munich, Germany with remote-first teams across the EU."},
    ]
    return faqs

@app.get("/jobs")
async def get_jobs():
    jobs = [
        {"id": "1", "title": "Senior Cloud Architect", "location": "Munich / Remote", "type": "Full-time"},
        {"id": "2", "title": "Data Engineer (Python)", "location": "Munich / Remote", "type": "Full-time"},
        {"id": "3", "title": "Cybersecurity Analyst", "location": "Munich / Remote", "type": "Full-time"},
        {"id": "4", "title": "Frontend Engineer (React)", "location": "Munich / Remote", "type": "Full-time"},
    ]
    return jobs
