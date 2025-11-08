import json
from pathlib import Path

CONFIG_DIR = Path("config")
DOC_CACHE = CONFIG_DIR / "documents.json"  # store all doc names + IDs here


def get_doc_id(sdk, api_key, document):
    """Return document_id for this document, creating it if needed."""
    doc_name = document["document_name"]

    # Load existing saved IDs (if file exists)
    if DOC_CACHE.exists():
        cache = json.loads(DOC_CACHE.read_text())
    else:
        cache = {}

    # If this doc is already saved, reuse its ID
    if doc_name in cache:
        print(f"Using cached ID for '{doc_name}': {cache[doc_name]}")
        return cache[doc_name]

    # Otherwise, create the doc and wait for it
    print(f"Creating new document for '{doc_name}'...")
    response = sdk.create_document(api_key=api_key, data=document)
    doc_id = response["document_id"]
    sdk.wait_until_document_ready(api_key, doc_id)

    # Save new doc name + ID to config/documents.json
    cache[doc_name] = doc_id
    DOC_CACHE.write_text(json.dumps(cache, indent=2))
    print(f"Saved '{doc_name}' → {doc_id} to {DOC_CACHE}")

    return doc_id
