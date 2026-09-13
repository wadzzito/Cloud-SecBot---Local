import subprocess
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from scanners.common.normalizer import normalize_kubescape_output, save_findings_json

def run_kubescape(target_path: str = "."):
    result = subprocess.run(
        ["kubescape", "scan", target_path, "--format", "json", "--output", "kubescape_raw.json"],
        capture_output=True, text=True
    )

    if not os.path.exists("kubescape_raw.json"):
        print("Kubescape no generó salida. stderr:", result.stderr)
        return []

    with open("kubescape_raw.json") as f:
        raw_json = json.load(f)

    findings = normalize_kubescape_output(raw_json)
    return findings

if __name__ == "__main__":
    findings = run_kubescape()
    save_findings_json(findings)
    print(f"Se encontraron {len(findings)} hallazgos en Kubernetes.")