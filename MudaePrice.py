import discord
import math
import re
from collections import deque
from time import sleep
import config
import sqlite3
from threading import Timer


client = discord.Client()
embeds = deque([], 10)
acceptedChannels = [863116140795396116]
PRICE_AUTOMARRY = 300
marry_enabled = False
kakera_grabber_enabled = False

KakeraList = ["KakeraP", "KakeraG", "KakeraY", "KakeraO", "KakeraR", "KakeraW", "KakeraL"]
KakeraList = [element.upper() for element in KakeraList]
print(KakeraList)


@client.event
async def on_ready():
	conn = sqlite3.connect('mudae.db')
	cursor = conn.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS roulette(
		category TEXT,
    	character TEXT UNIQUE,
    	gender INTEGER,
    	price INTEGER)
	""")
	conn.commit()

	MudaeChannel = client.get_channel(849723752065531945)
	#await MudaeChannel.send("$tu") #Say the price of the character

	print('Logged on as', client.user)


@client.event
async def on_message(message):
	global marry_enabled
	global kakera_grabber_enabled

	#if message.embeds == [] or message.embeds[0].to_dict()["color"] == undefined:
	#	return

	#849723752065531945
	#print(message.channel.id)
	if message.embeds != [] and (message.channel.id == 849723752065531945): #check for rolls
		embed = message.embeds[0].to_dict()

		if not "color" in embed.keys():
			return

		if "Rank".upper() in embed["description"].upper(): #If message is an im message
			return

		if "Rang".upper() in embed["description"].upper():
			return

		color = embed["color"]

		if color == 16751916: #If the message has a yellow bar (normal roll)
			character = embed["author"]["name"]
			print(character)

			addCharacterToEmbedsStack((character, message))
			await sendImMessage(character)


		if "Souhaité par" in message.content: #If message has a green bar (wish related)
			character = embed["author"]["name"]
			print(character)

			if not marry_enabled:
				return

			addCharacterToEmbedsStack((character, message))
			await sendImMessage(character)

			sleep(1)
			await message.add_reaction("jaichaud:849415484347645962") #Marry the character

			user = client.get_user(242677066372218881)

			sleep(2)
			await message.remove_reaction("jaichaud:849415484347645962", user)
			sleep(0.2)

			for i in range(10):
				await message.add_reaction("jaichaud:849415484347645962") #Marry the character
				await message.remove_reaction("jaichaud:849415484347645962", user) #Marry the character

			marry_enabled = False


	if message.embeds != [] and (message.channel.id == 863116140795396116): #Handle $im messages
		embed = message.embeds[0].to_dict()
		character = embed["author"]["name"]

		if not("Claim Rank" in embed["description"]): #If it's not an $im message, return
			return

		kakera_description = embed["description"].split("\n")

		found = False
		i = 0
		while not found and i < len(kakera_description):
			if kakera_description[i].find("**") != -1:
				kakera_description = kakera_description[i]
				found = True
			i += 1

		price = kakera_description #Keep the original description for future use
		price = price[price.find("**") + 2:]
		price = price[:price.find("**")]
		price = str(math.floor(int(price) * 1.52)) #The price on Tijimu's server is higher for some reason
		print(price)

		MudaeChannel = client.get_channel(863116140795396116)
		await MudaeChannel.send("GaybenSay " + character + " : " + price) #Say the price of the character


		category = kakera_description.split("·")[0]
		category = category[category.find("*") + 1:]
		category = category[:category.find("*")]

		gender_description = embed["description"].split("\n")

		found = False
		i = 0
		while not found and i < len(gender_description):
			if gender_description[i].find("<:male:452470164529872899>") != -1 or gender_description[i].find("<:female:452463537508450304>") != -1:
				gender_description = gender_description[i]
				found = True
			i += 1

		gender = 0
		if gender_description.find("<:male:452470164529872899>") != - 1:
			gender += 1
		if gender_description.find("<:female:452463537508450304>") != - 1:
			gender += 2


		addCharacterToDatabase(category, character, gender, price)

		if int(price) > PRICE_AUTOMARRY and marry_enabled: #If marry is available and the price is high enough
			for queueElement in embeds:
				queueCharacter, queueMessage = queueElement
				if queueCharacter == character:
					sleep(1)
					await queueMessage.add_reaction("jaichaud:849415484347645962") #Marry the character
					marry_enabled = False



	if message.channel.id == 849723752065531945 and "**Gayben**," in message.content and not "**@Mudaebot**" in message.content: #If message is for timers
		message.content = message.content.replace(':', '.')
		message.content = message.content.replace('!', '.')
		timers = message.content.split(".")

		if "__" in timers[0]:
			marry_enabled = True

		marryReset = timers[1]
		marryReset = marryReset[marryReset.find("**") + 2:]
		marryReset = marryReset[:marryReset.find("**")]

		r = Timer(convertTimerToMinutes(marryReset)*60.0, enableMarry, ())
		r.start()

		kakeraReset = timers[4]

		if "__" in kakeraReset:
			kakera_grabber_enabled = True
		else:
			kakeraReset = kakeraReset[kakeraReset.find("**") + 2:]
			kakeraReset = kakeraReset[:kakeraReset.find("**")]

			r = Timer(convertTimerToMinutes(kakeraReset)*60.0, enableKakeraGrabber, ())
			r.start()

		print("Timers : ")
		print("marry_enabled = " + str(marry_enabled))
		print("kakera_grabber_enabled = " + str(kakera_grabber_enabled))



		
@client.event
async def on_reaction_add(reaction, user): #Kakera grabber
	global kakera_grabber_enabled
	global KakeraList

	message = reaction.message

	if message.embeds != [] and (message.channel.id == 849723752065531945) and user.id == 432610292342587392 and kakera_grabber_enabled: #If message has an embed, in the right channel and from mudae
		embed = message.embeds[0].to_dict()

		if not "color" in embed.keys():
			return

		color = embed["color"]
		if ("kakera".upper() in str(reaction).upper()): #If the reaction is about a kakera

			kakeraType = str(message.reactions[0]).upper()
			kakeraType = kakeraType[kakeraType.find(":") + 1:]
			kakeraType = kakeraType[:kakeraType.find(":")]

			if message.reactions != [] and kakeraType in KakeraList:
				sleep(1)
				await message.add_reaction(message.reactions[0].emoji)
				kakera_grabber_enabled = False
				r = Timer(3*100*60.0, enableKakeraGrabber, ())
				r.start()


def enableMarry():
	global marry_enabled
	marry_enabled = True

	r = Timer(3*60*60.0, enableMarry, ())
	r.start()


def enableKakeraGrabber():
	global kakera_grabber_enabled
	kakera_grabber_enabled = True


def convertTimerToMinutes(timer):
	if "h" in timer:
		timer = timer.replace(" ", "")
		timer = timer.split("h")
		timer = int(timer[0]) * 60 + int(timer[1])

	return int(timer)


def addCharacterToEmbedsStack(element):
	global embeds
	embeds.appendleft(element)


async def sendImMessage(character):
	MudaeChannel = client.get_channel(863116140795396116)
	await MudaeChannel.send('$im ' + character)


def addCharacterToDatabase(category, character, gender, price):
	conn = sqlite3.connect('mudae.db')
	cursor = conn.cursor()
	data = {"category" : category, "character" : character, "gender" : gender, "price" : price}

	cursor.execute("""
	INSERT INTO roulette(category, character, gender, price) 
	VALUES(:category, :character, :gender, :price)
	ON CONFLICT(character)
	DO UPDATE SET price = :price;""", data)
	conn.commit()


def sandbox():
	print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	r = Timer(5.0, sandbox, ())
	r.start()
	



client.run(config.TOKEN)