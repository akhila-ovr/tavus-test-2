import sdk
import json
from cli import main as cli_main


def main():
    with open("secrets.json") as f:
        secrets = json.load(f)
    api_key = secrets["Tavus_API_Key"]

    persona, conversation, document = cli_main()

    print("Persona:", persona["persona_name"])
    print("Document:", document["document_name"])

    document_response = sdk.create_document(
        api_key=api_key,
        data=document,
    )

    sdk.wait_until_document_ready(api_key, document_response.get("document_id"))

    response = sdk.create_persona(api_key=api_key, data=persona)

    persona_id = response.get("persona_id")

    if persona_id:
        conv_response = sdk.create_conversation(
            api_key=api_key,
            data=conversation
            | {
                "persona_id": persona_id,
                "document_ids": [document_response.get("document_id")],
            },
        )
    print("Meeting Link:", conv_response["conversation_url"])


if __name__ == "__main__":
    main()
