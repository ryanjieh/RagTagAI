from google import genai
from google.genai import types

def query(prompt):
    client = genai.Client()
    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        content = prompt,
        config = types.GenerateContentConfig(
            system_instruction = [
                "You are a fashion recommendation system which takes a user's outfit and gives them improvements based on their style and lastest trends.",
                "Based on the context given, please output recommendations and improvements to their current outfit.",
                # Context here
            ]
        ),
    )
    return response.text

def main():
    print(query(input("Prompt: ")))

if __name__ == "__main__":
    main()