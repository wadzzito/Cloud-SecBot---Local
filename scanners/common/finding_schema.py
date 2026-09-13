from dataclasses import dataclass, asdict, field
from typing import Optional
import uuid

VALID_SEVERITIES = {"P0", "P1", "P2", "P3"}
VALID_MODULES = {"docker", "kubernetes", "terraform"}

@dataclass
class Finding:
    file_path: str
    rule_id: str
    rule_description: str
    severity: str                  # P0, P1, P2, P3
    source_module: str             # docker, kubernetes, terraform
    line_number: Optional[int] = None
    framework: Optional[str] = None      # CIS, OWASP, NSA-CISA
    resource_type: Optional[str] = None
    code_snippet: Optional[str] = None
    content_id: Optional[str] = None     # id del PR/issue en GitHub, lo llena el bot
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if self.severity not in VALID_SEVERITIES:
            raise ValueError(f"Severidad inválida: {self.severity}")
        if self.source_module not in VALID_MODULES:
            raise ValueError(f"Módulo inválido: {self.source_module}")

    def to_dict(self) -> dict:
        return asdict(self)


def severity_from_checkov(check_result: dict) -> str:
    """Checkov no siempre trae severidad clara — mapeo simple por defecto.
    Se puede refinar luego llamando a ai/claude_client.get_severity()"""
    severity_map = {
        "CRITICAL": "P0",
        "HIGH": "P1",
        "MEDIUM": "P2",
        "LOW": "P3",
    }
    raw = check_result.get("severity")
    return severity_map.get(raw, "P2")  # default P2 si no viene severidad

KNOWN_SEVERITY_OVERRIDES = {
    "CKV_DOCKER_1": "P1",   # puerto 22 expuesto
    "CKV_DOCKER_3": "P1",   # falta usuario no-root
    "CKV_DOCKER_7": "P3",   # imagen "latest" (menor urgencia)
    "CKV_AWS_23": "P0",     # ejemplo: security group abierto a 0.0.0.0/0
}

def severity_from_checkov(check_result: dict) -> str:
    check_id = check_result.get("check_id")
    if check_id in KNOWN_SEVERITY_OVERRIDES:
        return KNOWN_SEVERITY_OVERRIDES[check_id]

    severity_map = {"CRITICAL": "P0", "HIGH": "P1", "MEDIUM": "P2", "LOW": "P3"}
    raw = check_result.get("severity")
    return severity_map.get(raw, "P2")