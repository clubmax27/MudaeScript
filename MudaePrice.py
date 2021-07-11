import discord
import math
import re
from collections import deque
from time import sleep
import config


client = discord.Client()
embeds = deque([], 10)
acceptedChannels = [863116140795396116]
PRICE_AUTOMARRY = 300

marry_on_cooldown = True

@client.event
async def on_ready():
	print('Logged on as', client.user)


@client.event
async def on_message(message):
	#849723752065531945
	#print(message.channel.id)
	if message.embeds != [] and (message.channel.id == 849723752065531945):
		embed = message.embeds[0].to_dict()

		if "Rank".upper() in embed["description"].upper():
			return

		if "Rang".upper() in embed["description"].upper():
			return

		color = embed["color"]
		#print(color)

		sleep(0.5)

		if color == 16751916: #If the message has a yellow bar (normal roll)
			character = embed["author"]["name"]
			print(character)

			global embeds
			embeds.appendleft((character, message))

			MudaeChannel = client.get_channel(863116140795396116)
			await MudaeChannel.send('$im ' + character)


		if color == 611623: #If message has a green bar (wish related)
			character = embed["author"]["name"]
			print(character)

			if "Wishlist".upper() in character.upper(): #If someone uses $wishlist
				return

			if marry_on_cooldown:
				return

			await message.add_reaction("jaichaud:849415484347645962")


	if message.embeds != [] and (message.channel.id == 863116140795396116): #Handle $im messages
		embed = message.embeds[0].to_dict()
		character = embed["author"]["name"]

		if not("Claim Rank" in embed["description"]): #If it's not an $im message, return
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
		price = str(math.floor(int(price) * 1.52)) #The price on Tijimu's server is higher for some reason
		print(price)

		#await message.add_reaction("jaichaud:849415484347645962")

		MudaeChannel = client.get_channel(863116140795396116)
		await MudaeChannel.send("GaybenSay " + character + " : " + price) #Say the price of the character

		if int(price) > PRICE_AUTOMARRY and not marry_on_cooldown: #If marry is available and the price is high enough
			for queueElement in embeds:
				queueCharacter, queueMessage = queueElement
				if queueCharacter == character:
					sleep(0.5)
					await queueMessage.add_reaction("jaichaud:849415484347645962")

		
@client.event
async def on_reaction_add(reaction, user): #Kakera grabber
	message = reaction.message
	if message.embeds != [] and (message.channel.id == 849723752065531945) and user.id == 432610292342587392: #If message has an embed, in the right channel and from mudae
		embed = message.embeds[0].to_dict()
		color = embed["color"]
		print("color : " + str(color))

		if color == 6753288 and ("kakera".upper() in reaction.upper()): #If the color is Bordeau (already married roll)
			sleep(0.5)
			if message.reactions != []:
				await message.add_reaction(message.reactions[0].emoji)

client.run(config.TOKEN)