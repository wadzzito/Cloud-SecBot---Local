from scanners.common.finding_schema import Finding, severity_from_checkov


def normalize_checkov_output(raw_json: dict, source_module: str) -> list[Finding]:
    """Convierte el JSON crudo de Checkov al formato Finding estándar"""
    findings = []
    results = raw_json.get("results", {}).get("failed_checks", [])

    for check in results:
        finding = Finding(
            file_path=check.get("file_path", "desconocido"),
            line_number=check.get("file_line_range", [None])[0],
            rule_id=check.get("check_id", "N/A"),
            rule_description=check.get("check_name", "Sin descripción"),
            framework="CIS",
            severity=severity_from_checkov(check),
            source_module=source_module,
            resource_type=check.get("resource", None),
            code_snippet="\n".join(
                line[1] for line in check.get("code_block", [])
            ) if check.get("code_block") else None,
        )
        findings.append(finding)

    return findings


def normalize_kubescape_output(raw_json: dict) -> list[Finding]:
    """Convierte el JSON crudo de Kubescape al formato Finding estándar"""
    findings = []
    results = raw_json.get("results", [])

    for result in results:
        for control in result.get("controls", []):
            if control.get("status", {}).get("status") != "failed":
                continue

            finding = Finding(
                file_path=result.get("resourceID", "desconocido"),
                rule_id=control.get("controlID", "N/A"),
                rule_description=control.get("name", "Sin descripción"),
                framework="NSA-CISA",
                severity="P1",  # Kubescape maneja su propio scoring, se puede refinar
                source_module="kubernetes",
                resource_type=result.get("object", {}).get("kind", None),
            )
            findings.append(finding)

    return findings


def save_findings_json(findings: list[Finding], output_path: str = "findings_output.json"):
    """Guarda la lista normalizada en el archivo que consume bot/github_bot.py"""
    import json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([f.to_dict() for f in findings], f, ensure_ascii=False, indent=2)