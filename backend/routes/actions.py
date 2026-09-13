from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import crud
from ai.claude_client import get_fix_snippet
from ai.response_parser import parse_fix_response

router = APIRouter(prefix="/actions", tags=["actions"])

@router.post("/{finding_id}/apply-fix")
def apply_fix(finding_id: int, db: Session = Depends(get_db)):
    finding = crud.get_finding_by_id(db, finding_id)
    if not finding:
        return {"error": "No encontrado"}, 404

    finding_dict = {
        "file_path": finding.file_path,
        "line_number": finding.line_number,
        "rule_id": finding.rule_id,
        "rule_description": finding.rule_description,
        "framework": finding.framework,
        "severity": finding.severity,
        "code_snippet": finding.code_snippet,
    }

    raw_response = get_fix_snippet(finding_dict)
    parsed = parse_fix_response(raw_response)

    updated = crud.save_fix(
        db, finding_id,
        fixed_snippet=parsed["codigo_corregido"],
        explanation=parsed["explicacion"]
    )
    return updated

@router.post("/{finding_id}/dismiss")
def dismiss_finding(finding_id: int, db: Session = Depends(get_db)):
    """El usuario le dio 'Omitir' — aquí se decide la segunda advertencia"""
    updated = crud.update_finding_status(db, finding_id, "omitido")
    return updated

@router.post("/{finding_id}/mark-mitigated")
def mark_mitigated(finding_id: int, db: Session = Depends(get_db)):
    updated = crud.update_finding_status(db, finding_id, "mitigado")
    return updated