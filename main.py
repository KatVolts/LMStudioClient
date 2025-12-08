from LMStudioClient import *
if __name__ == "__main__":
    client = LMStudioClient()

    # NOTE: Ensure you have loaded a VISION model (like LLaVA or Pixtral) in LM Studio first!
    print("Models:", client.get_hosted_models())
    
    # 1. Text Only Query
    print("\n--- Text Query ---")
    print(client.query("What is the capital of France?"))

    #2. Image Query (Uncomment and set path to test)
    image_file = "C:\\Users\\katly\\Pictures\\Katbeach.jpg"
    if os.path.exists(image_file):
        print(f"\n--- Image Query ({image_file}) ---")
        response = client.query("Describe this image in detail.", image_path=image_file)
        print(response)