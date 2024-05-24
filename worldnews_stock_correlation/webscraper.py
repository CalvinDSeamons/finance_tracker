# Webscraper.py contains methods for scraping various websites, fromatting the data into json and saving it in txt or to the db. 
import praw


# Initialize the Reddit client
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent=''  # e.g., 'myapp by /u/yourusername'
)

# Define the subreddit and the type of posts you want to query
subreddit_name = 'learnpython'
subreddit = reddit.subreddit(subreddit_name)

# Example: Get the top 10 hot posts
top_posts = subreddit.hot(limit=5)

# Print the titles and comments of the top posts
for post in top_posts:
    print(f"Title: {post.title}")
    print(f"Score: {post.score}")
    print(f"URL: {post.url}")
    print(f"Comments:")
    post.comments.replace_more(limit=0)  # Replace "more comments" with actual comments
    for comment in post.comments.list():
        print(f"- {comment.body}")
    print("-" * 40)