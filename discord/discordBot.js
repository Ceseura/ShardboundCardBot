// Imports
const credentials = require('./credentials.js')
const Discord = require('discord.js')
const fs = require('fs')

ACTIVE_CHANNELS = [["channel-1", "channel-4"]]
ACTIVE_SERVERS = ["Bot testing"]
MY_ID = credentials.ID
// the bot's token - https://discordapp.com/developers/applications/me
const token = credentials.TOKEN

// The data from the .json file
var data
fs.readFile('../ShardBound_cards.json', 'utf8', function(err, fileData) {
	if (err) throw err
	console.log("File is ready!")
	data = JSON.parse(fileData)
})

// For printing purposes
var colors = JSON.parse('{"Neutral": "", "Steelsinger": "(Red) ", "Fatekeeper": "(Blue) ", "Landshaper": "(Green) ", "Packrunner": "(Yellow) ", "Wayfinder": "(Orange) ", "Bloodbinder": "(Purple) "}')

// create an instance of a Discord Client, and call it bot
const bot = new Discord.Client()

// the ready event is vital, it means that your bot will only start reacting to information from Discord _after_ ready is emitted.
bot.on('ready', () => {
  console.log('Bot is ready!')
});

// create an event listener for messages
bot.on('message', message => {

	// Is this a valid message that I want to respond to?
	do_me = false
	if (ACTIVE_SERVERS.indexOf(message.guild.name) > -1) {
		if (ACTIVE_CHANNELS[ACTIVE_SERVERS.indexOf(message.guild.name)].indexOf(message.channel.name) > -1) {
			do_me = true
		}
	}
	
	// Only work on ACTIVE_CHANNELS in ACTIVE_SERVERS and not the bot's messages
	if (do_me && message.author.id != MY_ID) {

		// REGEX match for [[CARD NAME]]
		var re = /\[\[[\d\w/' ,-]+\]\]/mig
		var matches = message.content.match(re)
		var reply = ""
		var amtProcessed = 0

		// If we found a [[CARD NAME]]
		if (matches != null) {
			console.log("Replying to:", message.author.username)
			console.log(matches)

			// Generate the reply
			for (var i in matches) {
				var cardName = matches[i].substring(2, matches[i].length-2).toLowerCase()

				// if the card is in the database
				if (data[cardName]) {
					card = data[cardName]
					if (card["type"] === "Melee Minion" || card["type"] === "Ranged Minion") {
						pReply = card["name"] + ": " + card["faction"] + " " + colors[card["faction"]] + card["rarity"] + " " + card["type"] + "\n" + card["mana"] + " Mana " + card["attack"] + "/" + card["health"] + " " + card["tribe"] + " - " + card["text"] + "\n\n"
					}

					if (card["type"] === "Melee Hero" || card["type"] === "Ranged Hero") {
						pReply = card["name"] + ": " + card["faction"] + " " + colors[card["faction"]] + card["type"] + "\n" + card["attack"] + "/" + card["health"] + " - " + card["text"] + "\n\n"
					}

					if (card["type"] === "Artifact Minion") {
						pReply = card["name"] + ": " + card["faction"] + " " + colors[card["faction"]] + card["rarity"] + " " + card["type"] + "\n" + card["mana"] + " Mana 0/" + card["health"] + " " + card["tribe"] + " - " + card["text"] + "\n\n"
					}

					if (card["type"] === "Spell") {
						pReply = card["name"] + ": " + card["faction"] + " " + colors[card["faction"]] + card["rarity"] + " " + card["type"] + "\n" + card["mana"] + " Mana - " + card["text"] + "\n\n"
					}

					reply += pReply
				}
			}
			message.channel.sendMessage(reply)

		}

  	}
});

// log our bot in
bot.login(token);