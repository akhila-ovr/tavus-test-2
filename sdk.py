import requests
from typing import Any, Dict, Iterable, Optional, List
import time


def make_request(method: str, url: str, api_key: str, data: Dict[str, Any]):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "GET":
            response = requests.get(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None),
        }


def create_persona(api_key: str, data: Dict[str, Any]):
    url = "https://tavusapi.com/v2/personas"
    return make_request("POST", url, api_key, data)


def create_conversation(api_key: str, data: Dict[str, Any]):

    url = "https://tavusapi.com/v2/conversations"
    return make_request("POST", url, api_key, data)


def create_document(api_key: str, data: Dict[str, Any]):

    url = "https://tavusapi.com/v2/documents"
    return make_request("POST", url, api_key, data)


def get_document_status(api_key: str, document_id: str):

    url = f"https://tavusapi.com/v2/documents/{document_id}"
    return make_request("GET", url, api_key, {})


def wait_until_document_ready(
    api_key: str, document_id: str, poll_secs: int = 5, timeout_secs: int = 300
) -> dict:
    """Poll until document reaches 'ready' or fails/timeout."""
    start = time.time()
    while True:
        info = get_document_status(api_key, document_id)
        status = info.get("status")
        print(f"[doc {document_id}] status: {status}")
        if status == "ready":
            return info
        if status == "failed":
            raise RuntimeError("Document processing failed")
        if time.time() - start > timeout_secs:
            raise TimeoutError("Timed out waiting for document to be ready")
        time.sleep(poll_secs)
