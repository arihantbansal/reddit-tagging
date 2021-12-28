from praw import Reddit
from praw.reddit import Subreddit
from psaw import PushshiftAPI
import csv
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.environ.get("reddit_client_id")  # Enter your client ID
client_secret = os.environ.get(
    "reddit_client_secret")  # Enter you client secret
username = os.environ.get("reddit_username")  # Enter Username
password = os.environ.get("reddit_password")  # Enter password

reddit = Reddit(client_id=client_id,
                client_secret=client_secret,
                user_agent='/r/news scraper by /u/' + username,
                username=username,
                password=password)

api = PushshiftAPI()

res = list(api.search_submissions(subreddit='news', filter=[
           'author', 'url', 'link_flair_richtext', 'title', 'upvote_ratio', 'selftext', 'permalink'], limit=10))


print(res)
