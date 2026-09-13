import os
import json
import requests
from bot.kanban_api import create_card, move_card, COLUMN_IDS

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ.get("GITHUB_REPOSITORY")        # ej. "usuario/cloud-secbot"
PR_NUMBER = os.environ.get("PR_NUMBER")            # lo pasas desde el workflow
API_URL = f"https://api.github.com/repos/{REPO}"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def post_comment(finding: dict):
    """Comenta el hallazgo + snippet corregido en el PR"""
    body = f"""### 🔎 Hallazgo de seguridad — {finding['severity']}

**Archivo:** `{finding['file_path']}` (línea {finding.get('line_number', '?')})
**Regla:** {finding['rule_id']} — {finding['rule_description']}

**Riesgo:** {finding.get('riesgo_si_no_se_corrige', 'No especificado')}

```diff
{finding.get('fixed_snippet', 'Sin sugerencia generada aún')}
```

_Generado automáticamente por Cloud SecBot._
"""
    url = f"{API_URL}/issues/{PR_NUMBER}/comments"
    response = requests.post(url, headers=HEADERS, json={"body": body})
    response.raise_for_status()
    return response.json()

def find_existing_comment(marker: str = "Cloud SecBot"):
    """Evita comentarios duplicados: busca si el bot ya comentó antes"""
    url = f"{API_URL}/issues/{PR_NUMBER}/comments"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    for comment in response.json():
        if marker in comment["body"]:
            return comment["id"]
    return None

def update_comment(comment_id: int, finding: dict):
    url = f"{API_URL}/issues/comments/{comment_id}"
    body = f"Actualizado — ver último hallazgo: {finding['rule_id']}"
    response = requests.patch(url, headers=HEADERS, json={"body": body})
    response.raise_for_status()
    return response.json()

def notify(findings: list[dict], project_id: str):
    """Punto de entrada: recibe la lista de hallazgos del scanner y notifica todo"""
    for finding in findings:
        existing = find_existing_comment()
        if existing:
            update_comment(existing, finding)
        else:
            post_comment(finding)

        # crea/mueve la tarjeta a "Hallazgos Nuevos"
        item_id = create_card(project_id, finding["content_id"])
        move_card(project_id, item_id, "STATUS_FIELD_ID", COLUMN_IDS["hallazgos_nuevos"])

if __name__ == "__main__":
    with open("findings_output.json") as f:
        findings = json.load(f)
    notify(findings, project_id=os.environ["PROJECT_ID"])