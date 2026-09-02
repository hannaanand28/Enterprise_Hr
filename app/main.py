"""
FastAPI backend for PulseHR AI — Next-Gen Workforce Intelligence & Retention Command.
"""
from fastapi import FastAPI
from app.api import attrition, dashboard, skills, policy, agent, career
from app.utils.logger import logger

app = FastAPI(
    title="PulseHR AI — Workforce Intelligence & Retention Command",
    description="Next-generation HR decision engine predicting employee attrition risk, generating AI retention playbooks, "
                "analyzing skill gaps, conducting policy simulation, and routing inquiries through intelligent agents.",
    version="2.0.0",
)

app.include_router(attrition.router)
app.include_router(dashboard.router)
app.include_router(skills.router)
app.include_router(policy.router)
app.include_router(agent.router)
app.include_router(career.router)


@app.on_event("startup")
def on_startup():
    logger.info("PulseHR AI Backend starting up")
    logger.info("ML inference pipeline & intelligence databases online")


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "PulseHR AI Intelligence Platform",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {"status": "healthy", "service": "PulseHR AI Engine"}

