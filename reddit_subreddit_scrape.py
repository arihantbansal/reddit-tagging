import praw
import csv
import codecs
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.environ.get("reddit_client_id")  # Enter your client ID
client_secret = os.environ.get(
    "reddit_client_secret")  # Enter you client secret
username = os.environ.get("reddit_username")  # Enter Username
password = os.environ.get("reddit_password")  # Enter password

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='/r/news scraper by /u/' + username,
                     username=username,
                     password=password)

reddit_home_url = 'https://www.reddit.com'

# subreddit = reddit.subreddit('news')

reddit_news_csv = codecs.open(
    'reddit_news.csv', 'w', 'utf-8')  # creating our csv file

# CSV writer for better formatting
subreddit_csv_writer = csv.writer(
    reddit_news_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
subreddit_csv_writer.writerow(
    ['ID', 'Name', 'URL', 'Upvotes', 'Upvote Ratio', 'Number of Comments', 'Flairs'])  # Column names


posts = reddit.subreddit('news').top('all', limit=20)

# for submission in reddit.subreddit('news').top("all", limit=20):
# print(submission.title)


def handle(posts):
  count = 1
  for post in posts:
    subr_name = 'news'
    url = reddit_home_url + post.permalink

    title = post.title
    nsfw = str(post.over_18)
    num_comments = post.num_comments
    upvotes = post.score
    upvote_ratio = post.upvote_ratio
    flair = post.link_flair_text

    print('Post #' + str(count) + ' is written to csv file.')
    subreddit_csv_writer.writerow(
        [str(count), title, url, upvotes, upvote_ratio, num_comments, nsfw, flair])

    count += 1


handle(posts)
reddit_news_csv.close()

print("\nCompleted!")
print("Top posts from /r/news are available in reddit_news.csv file.")
