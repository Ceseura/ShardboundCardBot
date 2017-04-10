import praw
import re
import json
import datetime
from credentials import USER_AGENT, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD

starttime = datetime.datetime.now().timestamp()

# This python script is a reddit bot which responds to submissions 
# with text formatted like '[[CARD NAME]]' with information about 
# the card, from www.shardveil.com/cards/. 

# Get the data from the .json file
with open("ShardBound_cards.json") as data_file:
	data = json.load(data_file)

# Dictionary for display purposes
colors = {"Neutral": "", "Steelsinger": "(Red)", "Fatekeeper": "(Blue)", "Landshaper": "(Green)", "Packrunner": "(Yellow)", "Wayfinder": "(Orange)", "Bloodbinder": "(Purple)"}


# {0} Card Name
# {1} Image Link
# {2} Faction
# {3} Type (Range/Melee)
# {4} Mana Cost
# {5} Attack Value
# {6} Health Value
# {7} Tribe
# {8} Rarity
# {9} Card Text
# {10} Color
MINION_REPLY_TEMPLATE = '[{0}]({1}) {2} {10} {8} {3}\n\n{4} Mana {5}/{6} {7} - {9}'
ARTIFACT_REPLY_TEMPLATE = '[{0}]({1}) {2} {10} {8} {3}\n\n{4} Mana 0/{6} {7} - {9}'
SPELL_REPLY_TEMPLATE = '[{0}]({1}) {2} {7} {5} {3}\n\n{4} Mana - {6}'
HERO_REPLY TEMPLATE = '[{0}]({1}) {2} {7} {3}\n\n{4}/{5} - {6}'
SIMPLE_TEMPLATE = "Card: {0}"


def main():
	# Initialize the Reddit Client
	reddit = praw.Reddit(user_agent=USER_AGENT, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD)

	# Which subreddit?
	subreddit = reddit.subreddit('Alex_is_a_Scrub')

	# Do stuff
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

	# Search for [[CARD NAME]] patterns
	pattern = re.compile('\[\[[a-z0-9 ]+\]\]')
	cardList = re.findall(pattern, text)
	print(cardList)

	for card in cardList:
		card = card[2:-2]
		# Make sure the card is valid
		if card in data:
			reply_text += generate_reply(data[card])
		else:
			print("Couldn't find", card)

	# Reply
	print("replying to", submission.title)
	submission.reply(reply_text)

def generate_reply(card):
	if "Artifact" in card["type"]:
		reply = MINION_REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["mana"], 0, card["health"], card["tribe"], card["rarity"], card["text"], colors[card["faction"]])

	elif "Minion" in card["type"]:
		reply = MINION_REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["mana"], card["attack"], card["health"], card["tribe"], card["rarity"], card["text"], colors[card["faction"]])

	elif "Spell" in card["type"]:
		reply = SPELL_REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["mana"], card["rarity"], card["text"], colors[card["faction"]])

	elif "Hero" in card["type"]:
		reply = HERO_REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["attack"], card["health"], card["text"], color[card["faction"]])

	else:
		reply = SIMPLE_TEMPLATE.format(card["name"])

	return reply

if __name__ == '__main__':
	main()