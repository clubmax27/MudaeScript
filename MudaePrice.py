import discord
import math
import re
from collections import deque
from time import sleep
import config


client = discord.Client()
embeds = deque([], 10)


@client.event
async def on_ready():
	print('Logged on as', client.user)

@client.event
async def on_message(message):
	acceptedChannels = [863116140795396116] #849723752065531945
	#print(message.channel.id)
	if message.embeds != [] and (message.channel.id == 849723752065531945):
		embed = message.embeds[0].to_dict()

		if "Rank".upper() in embed["description"].upper():
			return

		if "Rang".upper() in embed["description"].upper():
			return

		character = embed["author"]["name"]
		print(character)

		if "Wishlist".upper() in character.upper():
			return

		global embeds
		embeds.appendleft((character, message))


		MudaeChannel = client.get_channel(863116140795396116)
		await MudaeChannel.send('$im ' + character)


	if message.embeds != [] and (message.channel.id == 863116140795396116):
		embed = message.embeds[0].to_dict()
		character = embed["author"]["name"]

		if not("Claim Rank" in embed["description"]):
			return

		price = embed["description"].split("\n")

		found = False
		i = 0
		while not found and i < len(price):
			if price[i].find("**") != -1:
				price = price[i]
				found = True
			i += 1

		price = price[price.find("**") + 2:]
		price = price[:price.find("**")]
		price = str(math.floor(int(price) * 1.52))
		print(price)

		#await message.add_reaction("jaichaud:849415484347645962")

		MudaeChannel = client.get_channel(863116140795396116)
		await MudaeChannel.send("GaybenSay " + character + " : " + price)

		if int(price) > 200:
			for queueElement in embeds:
				queueCharacter, queueMessage = queueElement
				if queueCharacter == character:
					sleep(0.5)
					await queueMessage.add_reaction("jaichaud:849415484347645962")

		
        

client.run(config.TOKEN)