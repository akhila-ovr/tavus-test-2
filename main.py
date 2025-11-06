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

if __name__ == "__main__":
    main()
