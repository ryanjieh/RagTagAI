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

def find_relevant_posts(embed, k=5):
    pipeline = [
        {
            "$search": {
                "index": "vector_index",
                "knnBeta": {
                    "vector": embed,
                    "path": "embeds.values",
                    "k": k
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "image": 1,
                "image_embeds": 1,
                "text_embeds": 1,
                "embed": 1
            }
        }
    ]
    return list(collection.aggregate(pipeline))

# Close the client connection
client.close()