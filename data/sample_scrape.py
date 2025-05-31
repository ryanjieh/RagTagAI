import praw
import os
from dotenv import load_dotenv

load_dotenv()

def create_reddit_client():
    """
    Create and return a Reddit client using PRAW.
    Replace the placeholders with your Reddit API credentials.
    """
    reddit = praw.Reddit(
        client_id = os.getenv('CLIENT_ID'),
        client_secret = os.getenv('CLIENT_SECRET'),
        user_agent = 'ai fit check webapp by u/Minimum_Youth_5336 and more'
    )
    return reddit

def scrape_subreddit(subreddit_name, limit=10):
    """
    Scrape posts from a subreddit.
    :param subreddit_name: Name of the subreddit to scrape.
    :param limit: Number of posts to retrieve.
    :return: List of scraped posts.
    """
    reddit = create_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for post in subreddit.hot(limit=limit):
        posts.append({
            'title': post.title,
            'text': post.selftext,
            'score': post.score,
            'url': post.url,
            'created_utc': post.created_utc,
            'author': str(post.author),
            'images': [],
            'comments': []
        })
        
        # Check for single image posts
        if post.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            posts[-1]['images'].append(post.url)
            
        # Check for gallery posts
        if hasattr(post, 'media_metadata'):
            for item in post.media_metadata.values():
                if item['status'] == 'valid' and item['e'] in ['Image', 'AnimatedImage']:
                    posts[-1]['images'].append(item['s']['u'])

        # Get comments
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            posts[-1]['comments'].append({
                'author': str(comment.author),
                'body': comment.body,
                'score': comment.score,
                'created_utc': comment.created_utc
            })
            posts[-1]['comments'].sort(key = lambda x: x['score'], reverse = True)
    
    # Sort posts by score
    posts.sort(key = lambda x: x['score'], reverse = True)  
    return posts

def main():
    """
    Main function to demonstrate the scraper.
    """
    subreddit_names = ['streetwear']
    limit = 10  # Number of posts to scrape
    
    for subreddit_name in subreddit_names:
        
        print(f"Scraping subreddit: {subreddit_name}")
        
        posts = scrape_subreddit(subreddit_name, limit)

        for idx, post in enumerate(posts):
            print(f"Post {idx + 1}:")
            print(f"Title: {post['title']}")
            print(f"Description: {post['text'] if post['text'] else 'No description'}")
            print(f"Score: {post['score']}")
            print(f"URL: {post['url']}")
            print(f"Author: {post['author']}")
            print(f"Created UTC: {post['created_utc']}")
            print(f"Images: {', '.join(post['images']) if post['images'] else 'No images'}")
            print(f"Comments: {len(post['comments'])} comments")
            for comment in post['comments']:
                print(f"  - Comment by {comment['author']}: {comment['body']} (Score: {comment['score']})")
            print("-" * 80)

if __name__ == "__main__":
    main()