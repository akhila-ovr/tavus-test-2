import sdk 
import json

def main():
    with open('secrets.json') as f:
        secrets = json.load(f)

    document_response = sdk.create_document(
        api_key=secrets["Tavus_API_Key"],
        document_name="Test Document",
        document_url="https://arxiv.org/pdf/2503.18419"
    )
    print("Document Response:", document_response)

    sdk.wait_until_document_ready(secrets["Tavus_API_Key"], document_response.get("document_id"))

    response = sdk.create_persona(
        api_key=secrets["Tavus_API_Key"],
        persona_name="Test Persona",
        system_prompt="You are a helpful assistant.",
        context="User is testing the Tavus API."
    )
    print("API Response:", response)
    persona_id = response.get("persona_id")
    
    if persona_id:
        conv_response = sdk.create_conversation(
            api_key=secrets["Tavus_API_Key"],
            persogtina_id=persona_id,
            conversation_name="Test Conversation",
            document_ids=[document_response.get("document_id")] if document_response.get("document_id") else None
        )
        print("Conversation Response:", conv_response)

if __name__ == "__main__":
    main()
