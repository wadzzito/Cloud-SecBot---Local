from sqlalchemy.orm import Session
from models import Finding

def create_finding(db: Session, finding_data: dict) -> Finding:
    finding = Finding(**finding_data)
    db.add(finding)
    db.commit()
    db.refresh(finding)
    return finding

def get_findings(db: Session, status: str = None, severity: str = None):
    query = db.query(Finding)
    if status:
        query = query.filter(Finding.status == status)
    if severity:
        query = query.filter(Finding.severity == severity)
    return query.order_by(Finding.created_at.desc()).all()

def get_finding_by_id(db: Session, finding_id: int) -> Finding:
    return db.query(Finding).filter(Finding.id == finding_id).first()

def update_finding_status(db: Session, finding_id: int, new_status: str) -> Finding:
    finding = get_finding_by_id(db, finding_id)
    if finding:
        finding.status = new_status
        db.commit()
        db.refresh(finding)
    return finding

def save_fix(db: Session, finding_id: int, fixed_snippet: str, explanation: str) -> Finding:
    finding = get_finding_by_id(db, finding_id)
    if finding:
        finding.fixed_snippet = fixed_snippet
        finding.explanation = explanation
        finding.status = "en_validacion"
        db.commit()
        db.refresh(finding)
    return finding