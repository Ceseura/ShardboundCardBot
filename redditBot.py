import praw
import re
import json
import datetime

starttime = datetime.datetime.now().timestamp()

'''
{0} Card Name
{1} Image Link
{2} Faction
{3} Type (Range/Melee)
{4} Mana Cost
{5} Attack Value
{6} Health Value
{7} Tribe
{8} Rarity
{9} Card Text
{10} Color
'''

## TODO: doesn't respond to comments, only newly submitted posts


with open("ShardBound_cards.json") as data_file:
	data = json.load(data_file)

colors = {"Neutral": "", "Steelsinger": "(Red)", "Fatekeeper": "(Blue)", "Landshaper": "(Green)", "Packrunner": "(Yellow)", "Wayfinder": "(Orange)", "Bloodbinder": "(Purple)"}

REPLY_TEMPLATE = '[{0}]({1}) {2} {10} {8} {3}\n\n{4} Mana {5}/{6} {7} - {9}'
SIMPLE_TEMPLATE = "Card: {0}"

def main():
	reddit = praw.Reddit(user_agent='ShardBound Bot v0.1 (by /u/Cephael)', client_id='jOa76OEbDkSGcQ', client_secret='NKL_-ZYPuBqL_oTu5TUPGOpcIXc', username='Cephael', password='elephant1')

	subreddit = reddit.subreddit('Alex_is_a_Scrub')

	for submission in subreddit.stream.submissions():
		process_submission(submission)


def process_submission(submission):
	# Don't do anything if the comment was posted before the bot was started
	if starttime > submission.created_utc:
		print("skipped:", starttime, ">", submission.created_utc)
		return

	# Normalize text to lowercase
	text = submission.selftext.lower()
	print(text)
	pattern = re.compile('\[\[[a-z0-9 ]+\]\]')
	cardList = re.findall(pattern, text)
	print(cardList)

	for card in cardList:
		card = card[2:-2]
		if card in data:
			reply_text = generate_reply(data[card])
			print("replying to", submission.title)
			submission.reply(reply_text)
		else:
			print("Couldn't find", card)


def generate_reply(card):
	return REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["mana"], card["attack"], card["health"], card["tribe"], card["rarity"], card["text"], colors[card["faction"]])
	#return SIMPLE_TEMPLATE.format("blarp")

if __name__ == '__main__':
	main()