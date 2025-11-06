import requests
from typing import Iterable, Optional, List
import time

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

def create_conversation(
        api_key: str, 
        persona_id: str, 
        conversation_name: str = "Interview User",
        document_ids: Optional[Iterable[str]] = None,
        ):
    """
    Creates a new conversation for a given persona using the Tavus API.

    Args:
        api_key (str): Your Tavus API key.
        persona_id (str): The ID of the persona for which the conversation is created.
        conversation_name (str, optional): The name of the conversation. Defaults to "Interview User".
        document_ids (Optional[Iterable[str]]): Iterable of document ID strings returned by Create/Get Document.

    Returns:
        dict: Parsed JSON response from the API or an error message.
    """
    url = "https://tavusapi.com/v2/conversations"
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    data = {
        "persona_id": persona_id,
        "conversation_name": conversation_name,
    }

    if document_ids:
        data["document_ids"] = list(document_ids)   

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}

import requests

def create_document(api_key: str, document_name: str, document_url: str, callback_url: str = None):
    """
    Creates a document using the Tavus (or similar) API.

    Args:
        api_key (str): Your API key for authentication.
        document_name (str): The name of the document.
        document_url (str): The URL to the document file (e.g., a PDF).
        callback_url (str, optional): A webhook URL for progress updates.

    Returns:
        dict: JSON response from the API or an error message.
    """
    url = "https://tavusapi.com/v2/documents"  
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    # Prepare the request body
    data = {
        "document_name": document_name,
        "document_url": document_url,
    }

    # Only include callback_url if it’s provided
    if callback_url:
        data["callback_url"] = callback_url

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None)
        }

def get_document_status(api_key: str, document_id: str):
    """Get a document status from the API.

    Args:
        api_key: the Tavus API key
        document_id: the document id

    Returns:
        dict: parsed JSON response
    """
    url = f"https://tavusapi.com/v2/documents/{document_id}"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def wait_until_document_ready(api_key: str, document_id: str, poll_secs: int = 5, timeout_secs: int = 300) -> dict:
    """Poll until document reaches 'ready' or fails/timeout."""
    start = time.time()
    while True:
        info = get_document_status(api_key, document_id)
        status = (info.get("status") or "").lower()
        print(f"[doc {document_id}] status: {status}")
        if status == "ready":
            return info
        if status == "failed":
            raise RuntimeError("Document processing failed")
        if time.time() - start > timeout_secs:
            raise TimeoutError("Timed out waiting for document to be ready")
        time.sleep(poll_secs)