import json
import re

class InvalidClaudeResponse(Exception):
    pass

def _extract_json(raw_text: str) -> str:
    # quita bloques de código tipo ```json ... ```
    cleaned = re.sub(r"```json|```", "", raw_text).strip()
    return cleaned

def parse_fix_response(raw_text: str) -> dict:
    cleaned = _extract_json(raw_text)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise InvalidClaudeResponse(f"No se pudo parsear: {raw_text}")

    required_keys = {"explicacion", "codigo_corregido", "riesgo_si_no_se_corrige"}
    if not required_keys.issubset(data.keys()):
        raise InvalidClaudeResponse(f"Faltan campos en la respuesta: {data}")

    return data

def parse_severity_response(raw_text: str) -> dict:
    cleaned = _extract_json(raw_text)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise InvalidClaudeResponse(f"No se pudo parsear: {raw_text}")

    if data.get("severidad") not in {"P0", "P1", "P2", "P3"}:
        raise InvalidClaudeResponse(f"Severidad inválida: {data}")

    return data