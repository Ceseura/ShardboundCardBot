/*
  A ping pong bot, whenever you send "ping", it replies "pong".
*/

ACTIVE_CHANNELS = ["channel-1", "channel-4"]
ACTIVE_SERVERS = ["Bot testing"]
MY_ID = '301964200492793856'

// import the discord.js module
const Discord = require('discord.js')
var fs = require('fs')
var data

fs.readFile('../ShardBound_cards.json', 'utf8', function(err, fileData) {
	if (err) throw err
	console.log("File is ready!")
	data = JSON.parse(fileData)
})

colors = JSON.parse('{"Neutral": "", "Steelsinger": "(Red) ", "Fatekeeper": "(Blue) ", "Landshaper": "(Green) ", "Packrunner": "(Yellow) ", "Wayfinder": "(Orange) ", "Bloodbinder": "(Purple) "}')

// create an instance of a Discord Client, and call it bot
const bot = new Discord.Client()

// the token of your bot - https://discordapp.com/developers/applications/me
const token = 'MzAxOTY0MjAwNDkyNzkzODU2.C9Cr2Q.1mjt4m5kpk_3SyRg8qY9C_y_RNk'

// the ready event is vital, it means that your bot will only start reacting to information
// from Discord _after_ ready is emitted.
bot.on('ready', () => {
  console.log('Bot is ready!')
});

// create an event listener for messages
bot.on('message', message => {
	// Only work on ACTIVE_CHANNELS and ACTIVE_SERVERS and not the bot's messages
	if (ACTIVE_CHANNELS.indexOf(message.channel.name) > -1 && ACTIVE_SERVERS.indexOf(message.guild.name) > -1 && message.author.id != MY_ID) {

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