import sdk
import json
from utils.config_loader import load_config


def main():
    with open("secrets.json") as f:
        secrets = json.load(f)

    fashionAdvisor = load_config("personas", "fashionAdvisor")

    document_response = sdk.create_document(
        api_key=secrets["Tavus_API_Key"],
        data={
            "document_name": "test-doc-1",
            "document_url": "https://arxiv.org/pdf/2308.10385.pdf",
        },
    )
    print("Document Response:", document_response)

    sdk.wait_until_document_ready(
        secrets["Tavus_API_Key"], document_response.get("document_id")
    )

    response = sdk.create_persona(api_key=secrets["Tavus_API_Key"], data=fashionAdvisor)

    print("API Response:", response)
    persona_id = response.get("persona_id")

    if persona_id:
        conv_response = sdk.create_conversation(
            api_key=secrets["Tavus_API_Key"],
            data={
                "persona_id": persona_id,
                # "document_ids": [document_response.get("document_id")],
                "conversation_name": "Test Conversation 1",
            },
            persona_id=persona_id,
        )
        print("Conversation Response:", conv_response)


if __name__ == "__main__":
    main()
