import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODEL = "claude-sonnet-4-6"

def _load_prompt(prompt_file: str) -> str:
    base_path = os.path.join(os.path.dirname(__file__), "prompts", prompt_file)
    with open(base_path, "r", encoding="utf-8") as f:
        return f.read()

def get_fix_snippet(finding: dict) -> str:
    """
    finding debe traer: file_path, line_number, rule_id,
    rule_description, framework, severity, code_snippet
    """
    template = _load_prompt("fix_snippet_prompt.txt")
    prompt = template.format(**finding)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def get_severity(finding: dict) -> str:
    """
    finding debe traer: rule_id, rule_description, resource_type, context
    """
    template = _load_prompt("severity_prompt.txt")
    prompt = template.format(**finding)

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text