def find_relevant_posts(collection, embed, limit=5):
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": embed.squeeze().tolist(),
                "path": "embeds.values",
                "numCandidates": 100,
                "limit": limit
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "image": 1,
                "caption": 1,
                "sentiment": 1,
                "image_embeds": 1,
                "text_embeds": 1,
                "embed": 1
            }
        }
    ]
    return list(collection.aggregate(pipeline))