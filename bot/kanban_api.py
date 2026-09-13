import os
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GRAPHQL_URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

def _run_query(query: str, variables: dict) -> dict:
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()

def create_card(project_id: str, content_id: str) -> str:
    """Crea una tarjeta nueva en el proyecto (columna 'Hallazgos Nuevos' por default)"""
    query = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item { id }
      }
    }
    """
    variables = {"projectId": project_id, "contentId": content_id}
    result = _run_query(query, variables)
    return result["data"]["addProjectV2ItemById"]["item"]["id"]

def move_card(project_id: str, item_id: str, field_id: str, option_id: str):
    """Mueve una tarjeta a otra columna (status field) del Kanban"""
    query = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId,
        itemId: $itemId,
        fieldId: $fieldId,
        value: { singleSelectOptionId: $optionId }
      }) {
        projectV2Item { id }
      }
    }
    """
    variables = {
        "projectId": project_id,
        "itemId": item_id,
        "fieldId": field_id,
        "optionId": option_id
    }
    return _run_query(query, variables)

# IDs de las columnas — los obtienes una sola vez inspeccionando tu Project
# (te ayudo a sacarlos cuando tengas el tablero creado)
COLUMN_IDS = {
    "hallazgos_nuevos": "OPTION_ID_AQUI",
    "asignado": "OPTION_ID_AQUI",
    "en_validacion": "OPTION_ID_AQUI",
    "mitigado": "OPTION_ID_AQUI",
}