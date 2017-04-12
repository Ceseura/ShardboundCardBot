import praw
import re
import json
import datetime
from credentials import USER_AGENT2, CLIENT_ID2, CLIENT_SECRET2, USERNAME, PASSWORD

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
MINION_REPLY_TEMPLATE = '[{0}]({1}) {2} {10} {8} {3}\n\n{4} Mana {5}/{6} {7} - {9}\n\n\n'
ARTIFACT_REPLY_TEMPLATE = '[{0}]({1}) {2} {10} {8} {3}\n\n{4} Mana 0/{6} {7} - {9}\n\n\n'
SPELL_REPLY_TEMPLATE = '[{0}]({1}) {2} {7} {5} {3}\n\n{4} Mana - {6}\n\n\n'
HERO_REPLY_TEMPLATE = '[{0}]({1}) {2} {7} {3}\n\n{4}/{5} - {6}\n\n\n'
SIMPLE_TEMPLATE = "Card: {0}\n\n\n"

def main():
	# Initialize the Reddit Client
	reddit = praw.Reddit(user_agent=USER_AGENT2, client_id=CLIENT_ID2, client_secret=CLIENT_SECRET2, username=USERNAME, password=PASSWORD)

	# Which subreddit?
	subreddit = reddit.subreddit('Shardbound')

	# Do stuff
	for comment in subreddit.stream.comments():
		process_comment(comment)


def process_comment(comment):
	# Don't do anything if the comment was posted before the bot was started
	if starttime > comment.created_utc:
		print("skipped:", starttime, ">", comment.created_utc)
		return

	# Normalize text to lowercase
	text = comment.body.lower()
	print(text)

	# Search for [[CARD NAME]] patterns
	pattern = re.compile('\[\[[a-z0-9\' !-]+\]\]')
	cardList = re.findall(pattern, text)
	print(cardList)

	reply_text = ''
	for card in cardList:
		card = card[2:-2]
		# Make sure the card is valid
		if card in data:
			reply_text += generate_reply(data[card])
		else:
			print("Couldn't find", card)

	# Reply
	if reply_text is not '':
		print("replying to", comment.author)
		comment.reply(reply_text)

def generate_reply(card):
	if "Melee" in card["type"] or "Ranged" in card["type"]:
		reply = MINION_REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["mana"], card["attack"], card["health"], card["tribe"], card["rarity"], card["text"], colors[card["faction"]])

	if "Artifact" in card["type"]:
		reply = MINION_REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["mana"], 0, card["health"], card["tribe"], card["rarity"], card["text"], colors[card["faction"]])

	if "Spell" in card["type"]:
		reply = SPELL_REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["mana"], card["rarity"], card["text"], colors[card["faction"]])

	elif "Hero" in card["type"]:
		reply = HERO_REPLY_TEMPLATE.format(card["name"], card["link"], card["faction"], card["type"], card["attack"], card["health"], card["text"], colors[card["faction"]])

	return reply
	#return SIMPLE_TEMPLATE.format("blarp")

if __name__ == '__main__':
	main()