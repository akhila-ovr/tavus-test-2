import requests

def create_persona(
    api_key: str,
    persona_name: str,
    system_prompt: str,
    context: str,
    default_replica_id: str = "rfe12d8b9597",
    perception_model: str = "raven-0",
    smart_turn_detection: bool = True,
    pipeline_mode: str = "full"
):
    """
    Creates a persona using the Tavus API.

    Args:
        api_key (str): Your Tavus API key.
        persona_name (str): The name of the persona.
        system_prompt (str): The system prompt describing behavior.
        context (str): Additional context about the persona.
        default_replica_id (str): The default replica ID (default: rfe12d8b9597).
        perception_model (str): The perception model (default: raven-0).
        smart_turn_detection (bool): Enable smart turn detection (default: True).
        pipeline_mode (str): The pipeline mode (default: full).

    Returns:
        dict: Parsed JSON response from the API, or error info.
    """
    url = "https://tavusapi.com/v2/personas"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    data = {
        "persona_name": persona_name,
        "system_prompt": system_prompt,
        "pipeline_mode": pipeline_mode,
        "context": context,
        "default_replica_id": default_replica_id,
        "layers": {
            "perception": {"perception_model": perception_model},
            "stt": {"smart_turn_detection": smart_turn_detection},
        },
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}
