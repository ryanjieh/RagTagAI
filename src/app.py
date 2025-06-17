from flask import Flask, render_template, request
from PIL import Image
from embed import embed_user_input, generate_caption, combine_embeddings
from rating import embed_to_rating
from mongo import find_relevant_posts
from llm import query
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

uri = os.environ.get("MONGODB_URI")
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
client.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")
db = client["fit-check"]
collection = db["embeddings"]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rate", methods=["POST"])
def rate():
    # placeholder
    # Access uploaded image
    if 'image' not in request.files:
        print("No image file provided")
        return {"error": "No image file provided"}, 400
    try:
        image_file = request.files['image']
    except Exception as e:
        return {"error": "Invalid image file"}, 400
    image = Image.open(image_file)

    # Generate caption and embed image
    caption = generate_caption(image)
    print(caption)
    image_embed, text_embed = embed_user_input(image, caption)
    combined_embed = combine_embeddings(image_embed, text_embed)
    # print(combined_embed)
    
    # generate rating
    
    rating = embed_to_rating(combined_embed)
    rating = round(rating, 1)
    print(rating)
    
    # vector search for context
    
    relevant_posts = find_relevant_posts(collection, combined_embed, 5)
    
    # feed context to LLM
    user_outfit = {
        "image": image,
        "caption": caption
    }
    result = query(user_outfit, relevant_posts)
    result = f"Rating: {rating}\n\n" + result
    print(result)
    
    return {
        "result": result
    }

if __name__ == "__main__":
    app.run(debug=True)