import praw
import os
import sys
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv()

def human_readable_time(timestamp):
    """
    Convert a UTC timestamp to a human-readable format.
    :param timestamp: UTC timestamp.
    :return: Human-readable time string.
    """
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

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

    for i, post in enumerate(subreddit.hot(limit=limit)):
        posts.append({
            'title': post.title,
            'text': post.selftext,
            'score': post.score,
            'url': post.url,
            'created_utc': human_readable_time(post.created_utc),
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
        comments = post.comments.list()
        comments.sort(key=lambda x: x.score, reverse=True)
        for comment in comments[:min(5, len(comments))]:  # Limit to top 5 comments
            posts[-1]['comments'].append({
                'author': str(comment.author),
                'body': comment.body,
                'score': comment.score,
                'created_utc': human_readable_time(comment.created_utc)
            })
            posts[-1]['comments'].sort(key=lambda x: x['score'], reverse=True)
        print(f"Processed post {i + 1}/{limit} from subreddit: {subreddit_name}")
        
    # Sort posts by score
    posts.sort(key=lambda x: x['score'], reverse=True)
    return posts

def main():
    """
    Main function to demonstrate the scraper.
    """
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: py reddit_scraper.py subreddit_name limit [default=10]")
        sys.exit(1)
    
    subreddit_name = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) == 3 else 10  # Number of posts to scrape, default is 10

    print(f"Scraping subreddit: {subreddit_name}")
        
    posts = scrape_subreddit(subreddit_name, limit)

    if not posts:
        print(f"No posts found in subreddit: {subreddit_name}")
        return
        
    # Save posts to CSV
    print("=" * 50)
    print(f"Saving posts to CSV file...")
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(ROOT_DIR, "data", f"{subreddit_name}2.csv")
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['Title', 'Description', 'Score', 'URL', 'Author', 'Created UTC', 'Images', 'Comments'])
        for i, post in enumerate(posts):
            writer.writerow([
                post['title'],
                post['text'],
                post['score'],
                post['url'],
                post['author'],
                post['created_utc'],
                ', '.join(post['images']) if post['images'] else 'No images',
                   post['comments'] if post['comments'] else 'No comments'
               ])
            print(f"Saved post {i + 1}/{len(posts)}")
        print(f"Saved posts to {csv_file}")
        print(f"Scraped {len(posts)} posts from {subreddit_name}.")
        
if __name__ == "__main__":
    main()