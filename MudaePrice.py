import discord
import math
import re
from collections import deque
from time import sleep
import config
import sqlite3


client = discord.Client()
embeds = deque([], 10)
acceptedChannels = [863116140795396116]
PRICE_AUTOMARRY = 300
marry_on_cooldown = True


@client.event
async def on_ready():
	conn = sqlite3.connect('mudae.db')
	cursor = conn.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS roulette(
		category TEXT,
    	character TEXT UNIQUE,
    	price INTEGER)
	""")
	conn.commit()
	print('Logged on as', client.user)


@client.event
async def on_message(message):
	#849723752065531945
	#print(message.channel.id)
	if message.embeds != [] and (message.channel.id == 849723752065531945):
		embed = message.embeds[0].to_dict()

		if "Rank".upper() in embed["description"].upper(): #If message is an im message
			return

		if "Rang".upper() in embed["description"].upper():
			return

		color = embed["color"]
		#print(color)

		if color == 16751916: #If the message has a yellow bar (normal roll)
			character = embed["author"]["name"]
			print(character)

			addCharacterToEmbedsStack((character, message))
			await sendImMessage(character)


		if color == 611623: #If message has a green bar (wish related)
			character = embed["author"]["name"]
			print(character)

			if "Wishlist".upper() in character.upper(): #If someone uses $wishlist
				return

			if marry_on_cooldown:
				return

			addCharacterToEmbedsStack((character, message))
			await sendImMessage(character)

			sleep(0.5)
			await message.add_reaction("jaichaud:849415484347645962") #Marry the character


	if message.embeds != [] and (message.channel.id == 863116140795396116): #Handle $im messages
		embed = message.embeds[0].to_dict()
		character = embed["author"]["name"]

		if not("Claim Rank" in embed["description"]): #If it's not an $im message, return
			return

		description = embed["description"].split("\n")

		found = False
		i = 0
		while not found and i < len(description):
			if description[i].find("**") != -1:
				description = description[i]
				found = True
			i += 1

		price = description #Keep the original description for future use
		price = price[price.find("**") + 2:]
		price = price[:price.find("**")]
		price = str(math.floor(int(price) * 1.52)) #The price on Tijimu's server is higher for some reason
		print(price)

		MudaeChannel = client.get_channel(863116140795396116)
		await MudaeChannel.send("GaybenSay " + character + " : " + price) #Say the price of the character

		category = description.split("·")[0]
		category = category[category.find("*") + 1:]
		category = category[:category.find("*")]

		addCharacterToDatabase(category, character, price)

		if int(price) > PRICE_AUTOMARRY and not marry_on_cooldown: #If marry is available and the price is high enough
			for queueElement in embeds:
				queueCharacter, queueMessage = queueElement
				if queueCharacter == character:
					sleep(0.5)
					await queueMessage.add_reaction("jaichaud:849415484347645962") #Marry the character

		
@client.event
async def on_reaction_add(reaction, user): #Kakera grabber
	message = reaction.message
	if message.embeds != [] and (message.channel.id == 849723752065531945) and user.id == 432610292342587392: #If message has an embed, in the right channel and from mudae
		embed = message.embeds[0].to_dict()
		color = embed["color"]

		if color == 6753288 and ("kakera".upper() in str(reaction).upper()): #If the color is Bordeau (already married roll)
			if message.reactions != []:
				sleep(0.5)
				await message.add_reaction(message.reactions[0].emoji)


def addCharacterToEmbedsStack(element):
	global embeds
	embeds.appendleft(element)


async def sendImMessage(character):
	MudaeChannel = client.get_channel(863116140795396116)
	await MudaeChannel.send('$im ' + character)


def addCharacterToDatabase(category, character, price):
	conn = sqlite3.connect('mudae.db')
	cursor = conn.cursor()
	data = {"category" : category, "character" : character, "price" : price}

	cursor.execute("""
	INSERT INTO roulette(category, character, price) 
	VALUES(:category, :character, :price)
	ON CONFLICT(character)
	DO UPDATE SET price = VALUES(:price);""", data)
	conn.commit()


client.run(config.TOKEN)