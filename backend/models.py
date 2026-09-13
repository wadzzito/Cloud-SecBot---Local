from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    line_number = Column(Integer, nullable=True)
    rule_id = Column(String, nullable=False)
    rule_description = Column(Text, nullable=False)
    framework = Column(String, nullable=True)          # CIS, OWASP, etc.
    severity = Column(String, nullable=False)           # P0, P1, P2, P3
    code_snippet = Column(Text, nullable=True)
    fixed_snippet = Column(Text, nullable=True)         # respuesta de Claude
    explanation = Column(Text, nullable=True)
    status = Column(String, default="nuevo")            # nuevo, asignado, en_validacion, mitigado, omitido
    source_module = Column(String, nullable=False)       # docker, kubernetes, terraform
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)