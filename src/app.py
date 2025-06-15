from flask import Flask, render_template, request
from PIL import Image
from embed import embed_user_input, generate_caption, combine_embeddings
from llm import query

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
    image = Image.open(image_file.stream)

    # Generate caption and embed image
    caption = generate_caption(image)
    print(caption)
    # image_embed, text_embed = embed_user_input(image, caption)
    # combined_embed = combine_embeddings(image_embed, text_embed)
    
    # generate rating
    
    # vector search for context
    
    # feed context to LLM
    # result = query(context)
    
    return {
        "result": caption
    }

if __name__ == "__main__":
    app.run(debug=True)