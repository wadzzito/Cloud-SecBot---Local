import subprocess
import json
import sys
import os
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from scanners.common.normalizer import normalize_checkov_output, save_findings_json

def run_checkov_docker(target_path: str = "."):
    checkov_exe = shutil.which("checkov")
    if checkov_exe is None:
        raise FileNotFoundError(
            "No se encontró 'checkov' en el PATH. Verifica que esté instalado "
            "en tu entorno virtual con: pip install checkov"
        )

    result = subprocess.run(
        [checkov_exe, "-d", target_path, "--framework", "dockerfile", "-o", "json"],
        capture_output=True, text=True
    )

    if not result.stdout:
        print("Checkov no devolvió salida. stderr:", result.stderr)
        return []

    raw_json = json.loads(result.stdout)
    findings = normalize_checkov_output(raw_json, source_module="docker")
    return findings

if __name__ == "__main__":
    findings = run_checkov_docker()
    save_findings_json(findings)
    print(f"Se encontraron {len(findings)} hallazgos en Docker.")