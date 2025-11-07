import sdk 
import json

def main():
    with open('secrets.json') as f:
        secrets = json.load(f)

    # document_response = sdk.create_document(
    #     api_key=secrets["Tavus_API_Key"],
    #     document_name="Test Document",
    #     document_url="https://arxiv.org/pdf/2503.18419"
    # )
    # print("Document Response:", document_response)

    # sdk.wait_until_document_ready(secrets["Tavus_API_Key"], document_response.get("document_id"))

    response = sdk.create_persona(
        api_key=secrets["Tavus_API_Key"],
        data={
            "persona_name": "Fashion Advisor",
            "system_prompt": "As a Fashion Advisor, you specialize in offering tailored fashion advice.",
            "pipeline_mode": "full",
            "context": "You're having a video conversation with a client about their outfit.",
            "default_replica_id": "r79e1c033f",
            "layers": {
                "perception": {
                "perception_model": "raven-0",
                "ambient_awareness_queries": [
                    "Is the user wearing a bright outfit?"
                ],
                "perception_analysis_queries": [
                    "Is the user wearing multiple bright colors?",
                    "Is there any indication that more than one person is present?",
                    "On a scale of 1-100, how often was the user looking at the screen?"
                ],
                "perception_tool_prompt": "You have a tool to notify the system when a bright outfit is detected, named `notify_if_bright_outfit_shown`. You MUST use this tool when a bright outfit is detected.",
                "perception_tools": [
                    {
                    "type": "function",
                    "function": {
                        "name": "notify_if_bright_outfit_shown",
                        "description": "Use this function when a bright outfit is detected in the image with high confidence",
                        "parameters": {
                        "type": "object",
                        "properties": {
                            "outfit_color": {
                            "type": "string",
                            "description": "Best guess on what color of outfit it is"
                            }
                        },
                        "required": ["outfit_color"]
                        }
                    }
                    }
                ]
                }
            }
            }
    )
    print("API Response:", response)
    persona_id = response.get("persona_id")
    
    if persona_id:
        conv_response = sdk.create_conversation(
            api_key=secrets["Tavus_API_Key"],
            persona_id=persona_id,
            conversation_name="Test Conversation",
            # document_ids=[document_response.get("document_id")] if document_response.get("document_id") else None,
            document_ids=["d5-5f945d064899"],
            properties={
                "enable_closed_captions": True,
                "apply_greenscreen": False,
                "max_call_duration": 60,           # 1 minute
                "participant_left_timeout": 60,      # End call if user leaves for 1 min
                "participant_absent_timeout": 120    # End call if user inactive for 2 min
            }
        )
        print("Conversation Response:", conv_response)

if __name__ == "__main__":
    main()
