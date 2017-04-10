from lxml import html
import requests
from imgurpython import ImgurClient

# ALL DATA TAKEN FROM www.shardveil.com

# Used to upload card pictures to imgur. 
#client = ImgurClient(#client_id, #client_secret)

# The json file
myfile = open("myFile.json", "w")
myfile.write("{\n")

# Formatted like this

# "novice knight": {
# 	  "name": "Novice Knight",
# 	  "link": "https://www.google.com",
# 	  "faction": "Neutral",
# 	  "type": "Melee",
# 	  "mana": 1,
# 	  "attack": 2,
# 	  "health": 2,
# 	  "tribe": "",
#	  "rarity": Basic
# 	  "text": "Deathhowl: Add angry dude to hand"
# 	},

TEMPLATE = '	"{0}": {{\n\
		"name": "{1}", \n\
		"link": "{2}", \n\
		"faction": "{3}", \n\
		"type": "{4}", \n\
		"mana": "{5}", \n\
		"attack": "{6}", \n\
		"health": "{7}", \n\
		"tribe": "{8}", \n\
		"rarity": "{9}", \n\
		"text": "{10}" \n\
		}},\n'

BASE_URL = "https://www.shardveil.com"
#CLASSES = ["/cards/neutral.php"]
CLASSES = ["/cards/neutral.php", "/cards/steelsinger.php", "/cards/fatekeeper.php", "/cards/landshaper.php", "/cards/bloodbinder.php", "/cards/packrunner.php", "/cards/wayfinder.php"]

def escapeMe(mystr):
	for index in range(len(mystr)-1, -1, -1):
		if mystr[index] == '"':
			mystr = mystr[:index] + "\\" + mystr[index:]


	return mystr

for clas in CLASSES:
	print("Working on class", clas)
	# Get the page with all the class' cards
	page = requests.get(BASE_URL + clas)
	tree = html.fromstring(page.content)

	# Get all the cards' subpages' URLs
	cards = tree.xpath('//div[contains(@class, "mix")]/a/@href')

	for card in cards:
		print("Working on card", card)
		# Go to subpage
		page = requests.get(BASE_URL + card)
		tree = html.fromstring(page.content)

		# Card name
		name = card[7:].replace('-', ' ').title()

		# Card info, in a list
		#info = tree.xpath('//div[@class="card_details"]/p/text()')
		search = '//div[@class="card_details"]/p/text() | //div[@class="card_details"]/p/b/text() | //div[@class="card_details"]/p/span/b/text()'
		info = tree.xpath(search)

		# Clean up the list

		try: 
			info.remove('Faction: ')
		except: 
			pass
		try: 
			info.remove('Type: ')
		except: 
			pass
		try: 
			info.remove('Cost: ')
		except: 
			pass
		try: 
			info.remove('Health: ')
		except: 
			pass
		try: 
			info.remove('Damage: ')
		except: 
			pass
		try: 
			info.remove('Rarity: ')
		except: 
			pass
		try: 
			info.remove('Description: ')
		except:
			pass

		# Card image
		image_url = tree.xpath('//div[@class="card_img"]/img/@src')


		# Upload image to rehost independently on imgur
		#uploaded_image = client.upload_from_url(BASE_URL + image_url[0])
		#image_link = "https://imgur.com/" + uploaded_image["id"] + ".jpg"
		image_link = BASE_URL + image_url[0]

		# Parse info for different types of cards (minion, artifact, spell)

		attack = ""
		health = ""
		tribe = ""

		# Is a minion
		if info[1] == " Melee Minion" or info[1] == " Ranged Minion" or info[1] == " Ranged Hero" or info[1] == " Melee Hero":

			info[6] = ''.join(info[6:])
			info = info[:7]

			for index in range(len(info)):
				info[index] = info[index][1:]

			faction = info[0]
			mtype = info[1]
			mana = info[2]
			attack = info[4]
			health = info[3]
			rarity = info[5]
			text = info[6]

		# Is an artifact
		if info[1] == " Artifact Minion":

			info[5] = ''.join(info[5:])
			info = info[:6]

			for index in range(len(info)):
				info[index] = info[index][1:]

			faction = info[0]
			mtype = info[1]
			mana = info[2]
			health = info[3]
			rarity = info[4]
			text = info[5]

		# Is a spell
		if info[1] == " Spell":

			info[4] = ''.join(info[4:])
			info = info[:5]

			for index in range(len(info)):
				info[index] = info[index][1:]

			faction = info[0]
			mtype = info[1]
			mana = info[2]
			rarity = info[3]
			text = info[4]

		# Write to json file
		myfile.write(TEMPLATE.format(name.lower(), name, image_link, faction, mtype, mana, attack, health, tribe, rarity, escapeMe(text)))


myfile.write("\n}")
myfile.close()