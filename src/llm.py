from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
load_dotenv()

client = client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

instruction = [
                "You are a fashion recommendation system which takes a user's outfit and gives them improvements based on their style and lastest trends.",
                "The user will provide his outfit as well as reddit posts containing captions of similar outfits and a sentiment rating from 1 to 5, with 1 being the worst and 5 being the best. Based on the above, output recommendations and improvements to their current outfit.",
                "Your answer should only contain the suggestions and nothing else. There should not be any text styles or font modifications such as bold and italics, or bullet points, just lines of suggestions. Separation between suggestions should contain an additional newline."
            ]

def pil_image_to_bytes(image, format):
    buf = BytesIO()
    image.save(buf, format = format[6:])
    return buf.getvalue()

def query(user_outfit, relevant_posts):
    image_format = Image.MIME[user_outfit["image"].format]
    image_data = pil_image_to_bytes(user_outfit["image"], image_format)
    image = types.Part.from_bytes(
        data = image_data,
        mime_type = image_format
    )
    prompt = [
        image,
        "This is my outfit. Below are some Reddit posts of similar outfits each with captions and sentiment ratings from 1 to 5:",
    ]
    for i, post in enumerate(relevant_posts):
        num = f"{i + 1}."
        caption = post["caption"]
        sentiment = f"{post["sentiment"]}"
        prompt.append(num)
        prompt.append(caption)
        prompt.append(sentiment)
    
    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents = prompt,
        config = types.GenerateContentConfig(
            system_instruction = instruction
        ),
    )
    return response.text

def main():
    print(query(input("Prompt: ")))

if __name__ == "__main__":
    main()