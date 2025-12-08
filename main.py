from LMStudioClient import *

if __name__ == "__main__":
    client = LMStudioClient()
    
    # 1. High Temperature (Creative)
    print("--- Creative Response (Temp 0.9) ---")
    response_creative = client.query(
        "Give me a unique name for a pet dragon.", 
        temperature=0.9
    )
    print(response_creative)

    # 2. Low Temperature (Deterministic/Precise)
    print("\n--- Precise Response (Temp 0.1) ---")
    response_precise = client.query(
        "What is 2 + 2?", 
        temperature=0.1
    )
    print(response_precise)