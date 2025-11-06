import sdk 
import json

def main():
    with open('secrets.json') as f:
        secrets = json.load(f)
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
            persona_id=persona_id,
            conversation_name="Test Conversation"
        )
        print("Conversation Response:", conv_response)

if __name__ == "__main__":
    main()
