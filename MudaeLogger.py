import discord
import math
import re
from collections import deque
from time import sleep
import config
import sqlite3
from threading import Timer
import time


client = discord.Client()
acceptedChannels = [863116140795396116]


@client.event
async def on_ready():
	conn = sqlite3.connect('mudae.db')
	cursor = conn.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS roulette(
		category TEXT,
    	character TEXT UNIQUE,
    	gender INTEGER,
    	price INTEGER,
    	dropCount INTEGER);
	""")
	conn.commit()

	cursor.execute("""
    	CREATE TABLE IF NOT EXISTS dateLogging(
    	character TEXT,
    	timestamp INTEGER,
    	isWish BOOL);
	""")
	conn.commit()

	MudaeChannel = client.get_channel(849723752065531945)
	#await MudaeChannel.send("$tu") #Say the price of the character

	print('Logged on as', client.user)

@client.event
async def on_message(message):
	#print(message)

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

			await sendImMessage(character)
			addRollToDatabase(character, False)


		if "Souhaité par" in message.content: #If message has a green bar (wish related)
			character = embed["author"]["name"]
			print(character)

			await sendImMessage(character)
			addRollToDatabase(character, True)


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
		price = str(math.floor(int(price) * 1.6) + 1)  #The price on Tijimu's server is higher for some reason
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


async def sendImMessage(character):
	MudaeChannel = client.get_channel(863116140795396116)
	await MudaeChannel.send('$im ' + character)


def addCharacterToDatabase(category, character, gender, price):
	conn = sqlite3.connect('mudae.db')
	cursor = conn.cursor()

	dropCount = 0

	cursor.execute("""SELECT character, dropCount FROM roulette""")
	rows = cursor.fetchall()
	for row in rows:
		if(row[0] == character):
			dropCount = row[1]

	if dropCount == 0:
		data = {"category" : category, "character" : character, "gender" : gender, "price" : price}

		cursor.execute("""
		INSERT INTO roulette(category, character, gender, price, dropCount) 
		VALUES(:category, :character, :gender, :price, 1);""", data)
		conn.commit()

	else:
		data = {"character" : character, "price" : price, "dropCount" : dropCount + 1}

		cursor.execute("""UPDATE roulette SET price = :price, dropCount = :dropCount WHERE character = :character""", data)
		conn.commit()
	

def addRollToDatabase(character, isWish):
	conn = sqlite3.connect('mudae.db')
	cursor = conn.cursor()

	data = {"character" : character, "timestamp" : int(time.time()), "isWish" : isWish}

	cursor.execute("""
	INSERT INTO dateLogging(character, timestamp, isWish) 
	VALUES(:character, :timestamp, :isWish);""", data)
	conn.commit()

client.run(config.TOKEN)