from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud

router = APIRouter(prefix="/findings", tags=["findings"])

@router.get("/")
def list_findings(status: str = None, severity: str = None, db: Session = Depends(get_db)):
    findings = crud.get_findings(db, status=status, severity=severity)
    return findings

@router.get("/{finding_id}")
def get_finding(finding_id: int, db: Session = Depends(get_db)):
    finding = crud.get_finding_by_id(db, finding_id)
    if not finding:
        return {"error": "No encontrado"}, 404
    return finding

@router.get("/pending-alerts/")
def get_pending_alerts(db: Session = Depends(get_db)):
    """Lo que consulta el desktop-app para saber si debe abrir la pantalla fullscreen"""
    findings = crud.get_findings(db, status="nuevo")
    return findings