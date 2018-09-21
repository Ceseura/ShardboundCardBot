import praw
import sys
import datetime
from credentials import USERNAME, PASSWORD, USER_AGENT_DEBUG, CLIENT_ID_DEBUG, CLIENT_SECRET_DEBUG

LOG_TEMPLATE = "{4} Detected {3} Responded to {0}'s {1} {2}.\n"

li = ["hello", "world"]

def main():
	filename = 'logfile.txt'
	logfile = open(filename, 'w')

	reddit = praw.Reddit(user_agent=USER_AGENT_DEBUG, client_id=CLIENT_ID_DEBUG, client_secret=CLIENT_SECRET_DEBUG, username=USERNAME, password=PASSWORD)

	subreddit = reddit.subreddit('Alex_is_a_scrub')
	limit = 0


	for item in subreddit.stream.submissions():
		print(vars(item))
		if limit > 5: break
		limit += 1

		time = datetime.datetime.now()
		itemType = "submission"
		author = item.author
		myId = item.permalink
		logfile.write(LOG_TEMPLATE.format(author, itemType, myId, li, time))



if __name__ == '__main__':
	main()