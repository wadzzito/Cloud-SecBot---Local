import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from db.database import SessionLocal, init_db
from db import crud

init_db()
db = SessionLocal()

crud.create_finding(db, {
    "file_path": "docker/Dockerfile",
    "line_number": 13,
    "rule_id": "CKV_DOCKER_1",
    "rule_description": "Puerto 22 expuesto a internet",
    "framework": "CIS",
    "severity": "P0",
    "code_snippet": "EXPOSE 22",
    "source_module": "docker",
    "status": "nuevo",
})

print("Hallazgo de prueba insertado.")
db.close()