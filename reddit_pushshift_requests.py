import pandas as pd
import requests
import json
import csv
import time
import datetime


# Adapted from this https://gist.github.com/dylankilkenny/3dbf6123527260165f8c5c3bc3ee331b
# This function builds an Pushshift URL, accesses the webpage and stores JSON data in a nested list
def getPushshiftData(sub):
  # Build URL
  url = 'https://api.pushshift.io/reddit/search/submission/?size=1000&subreddit=' + \
      str(sub)
  # Print URL to show user
  print(url)
  # Request URL
  r = requests.get(url)
  # Load JSON data from webpage into data variable
  data = json.loads(r.text)
  # return the data element which contains all the submissions data
  return data['data']

# This function will be used to extract the key data points from each JSON result


def collectSubData(subm):
  # subData was created at the start to hold all the data which is then added to our global subStats dictionary.
  subData = list()  # list to store data points
  title = subm['title']
  url = subm['url']
  # flairs are not always present so we wrap in try/except
  try:
    flair = subm['link_flair_text']
  except KeyError:
    flair = "NaN"
  author = subm['author']
  sub_id = subm['id']
  score = subm['score']
  created = datetime.datetime.fromtimestamp(
      subm['created_utc'])  # 1520561700.0
  numComms = subm['num_comments']
  permalink = subm['permalink']

  # Put all data points into a tuple and append to subData
  subData.append((sub_id, title, url, author, score,
                 created, numComms, permalink, flair))
  # Create a dictionary entry of current submission data and store all data related to it
  subStats[sub_id] = subData


# Create your timestamps and queries for your search URL
# https://www.unixtimestamp.com/index.php > Use this to create your timestamps
# Submissions after this timestamp (1577836800 = 01 Jan 20)
# after = "1577836800"
# Submissions before this timestamp (1607040000 = 04 Dec 20)
# before = "1607040000"
# query = "Cyberpunk 2077"  # Keyword(s) to look for in submissions
sub = "news"  # Which Subreddit to search in

# subCount tracks the no. of total submissions we collect
subCount = 0
# subStats is the dictionary where we will store our data.
subStats = {}


# We need to run this function outside the loop first to get the updated after variable
data = getPushshiftData(sub)
# Will run until all posts have been gathered i.e. When the length of data variable = 0
# from the 'after' date up until before date
# The length of data is the number submissions (data[0], data[1] etc), once it hits zero (after and before vars are the same) end
for submission in data:
  collectSubData(submission)

print(len(data))

print(str(len(subStats)) + " submissions have added to list")
print("1st entry is:")
print(list(subStats.values())[0][0][1] +
      " created: " + str(list(subStats.values())[0][0][5]))
print("Last entry is:")
print(list(subStats.values())[-1][0][1] +
      " created: " + str(list(subStats.values())[-1][0][5]))


def updateSubs_file():
  upload_count = 0
  # location = "\\Reddit Data\\" >> If you're running this outside of a notebook you'll need this to direct to a specific location
  print("Input filename of submission file, please add .csv")
  filename = input()  # This asks the user what to name the file
  file = filename
  with open(file, 'w', newline='', encoding='utf-8') as file:
    a = csv.writer(file, delimiter=',')
    headers = ["Post ID", "Title", "URL", "Author", "Score",
               "Publish Date", "Total No. of Comments", "Permalink", "Flair"]
    a.writerow(headers)
    for sub in subStats:
      a.writerow(subStats[sub][0])
      upload_count += 1

    print(str(upload_count) + " submissions have been uploaded")


updateSubs_file()
