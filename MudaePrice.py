import discord
import math
import re
from collections import deque
from time import sleep
import sqlite3
from threading import Timer
import time
import asyncio
import sys

client = discord.Client()
embeds = deque([], 10)
acceptedChannels = [863116140795396116]

PRICE_AUTOMARRY = 400

marry_enabled = False
kakera_grabber_enabled = False

timerMarry = Timer(1000000, (), ())
timerKakera = Timer(1000000, (), ())

timerMarry.start()
timerKakera.start()

KakeraList = ["KakeraY", "KakeraO", "KakeraR", "KakeraW", "KakeraL"]
KakeraList = [element.upper() for element in KakeraList]

WishList = [#"Hyo-in Lee", "Sungjoon Bae", "Yeonsoo Lee", "Bin Joo", #Make me bark
			"Azusa Hamaoka", "Necai Sys", "Iris Heart", #Purple bitch
			#"Alexis Leskinen", "Eisuke Urushibara", "Judy Reyes", "Kaede Kurushima", "Kagari Shiina", "Katsumi Nakase", "Kayano", "Kuroki", "Maho Hiyajo", "Nae Tennouji", "Nakabachi", "Street Vendor", "Yuki Amane", "Yukitaka Akiha", "Yuugo Tennouji", "Moeka Kiryuu", "Itaru Hashida", #Steins;Gate
			"Ganon (CDi)", "Gwonam", "King Harkinian", "Link (CDi)", "Morshu", "Zelda (CDi)", #Zelda CDi Series
			"Sebastian", "Leah (SDV)", "Penny (SDV)", "Haley", "Harvey", #stardew valley
			"Pulptenks Flanders", #cute girls
			"Madeline", "Badeline", #"Theo", "Old Woman", "Mr. Oshiro", #Celeste
			#"Buttercup", "Tails", "Chat Noir", "Jessie", "Felindra",  #Collection de Duos/Trios
			"Faker", "Sneaky", "Tryndamere", #League of Legends
			#"Reuben (MCSM)", "Brody Foxx", "Linus Sebastian", "Splat Tim", "RNGesus", #Memes
			"Emmanuel Macron", "Marine Le Pen", "Jean-Marie Le Pen", #political figures
			"Kat (P&C)", "Catra", "Annie Brown", #Vol honteux (Laffey)
			"Azazel (HT)", "Beelzebub (HT)", "Helltaker", "Judgement", "Justice", "Lucifer", "Malina", "Modeus", "Pandemonica", "Subject 67", "Zdrada", #Helltaker
			#"Marvin", "Tiara (Petscop)", #Petscop
			"BMO", "Princess Finn", "Princess Bubblegum", "Marceline", #Adventure Time
			"Aelita", #"Yumi Ishiyama", "Odd Della Robbia", "Ulrich Stern", "Franz Hopper", "Jim Moralès", "Jeremie Belpois", #Code Lyoko
			"Rainbow Dash", "Element of Kindness", "Twilight Sparkle", "Pinkie Pie", "Rarity", "Applejack", "Princess Luna", "Princess Celestia", "Discord", "Sunset Shimmer", "Starlight Glimmer",  #MLP
			"Hime Hajime", "Veibae", #VShojo (Laffey)
			#"Alice Mizuki", "Mika Iwakura", "Chisa Yomoda", "Reika Yamamoto", "Juri Katou (SEL)", "Karl Haushofer", "Lin Sui-Xi", "Masami Eiri", "Miho Iwakura", "Myu-Myu", "Taro", "Yasuo Iwakura", #Serial Experiments Lain
			#"Ashley Rosemarry", "Nikki Ann-Marie", "Aiko Yumi", "Jessie Maye", "Audrey Belrose", "Theiatena Venus", "Momo (HP)", "Celeste Luvendass", "Tiffany Maye", "Lola Rembrite", "Beli Lapran" #HuniePop
			"Bill Cipher", "Dipper Pines", "Waddles", "Ford Pines", "Soos Ramirez",  "Gideon Gleeful", #"Giffany", "Pacifica Northwest", "Shmebulock", "Fiddleford McGucket", "Robbie Valentino", "Gompers", "Candy Chiu", #"8 Ball", "Blendin Blandin", "Tyler Cutebiker", "Justin Kerprank", #Gravity Falls
			"Hat Kid", #"Rumbi", "Bow Kid", "Snatcher", "The Conductor", "Mustache Girl", "DJ Grooves", "Cooking Cat", "The Empress", "Mafia Boss", "Badge Seller", #A Hat In Time
			"Acca", "Ai Ohto", "Chiaki Kawai", "Frill", "Kaoru Kurita", "Kirara (WEP)", "Koito Nagase", "Kotobuki Awano", "Kurumi Saijo", "Leon (WEP)", "Mako (WEP)", "Mannen", "Miko (WEP)", "Minami Suzuhara", "Misaki Tanabe", "Momoe Sawaki", "Neiru Aonuma", "Panic", "Pinky (WEP)", "Rika Kawai", "Shuichirou Sawaki", "Tae Ohto", "Ura-Acca", "Yae Yoshida"] #Wonder Egg Priority

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

	MudaeChannel = client.get_channel(863116140795396116)
	await MudaeChannel.send("$tu") #Say the price of the character

	print('Logged on as', client.user)

@client.event
async def on_message(message):
	sys.stdout.flush()
	#print(message)

	global marry_enabled
	global kakera_grabber_enabled

	global timerMarry
	global timerKakera

	global WishList

	#if message.embeds == [] or message.embeds[0].to_dict()["color"] == undefined:
	#	return

	#849723752065531945
	#print(message.channel.id)
	if message.embeds != [] and (message.channel.id == 849723752065531945): #check for rolls
		embed = message.embeds[0].to_dict()

		if "prendra grand soin de".upper() in message.content.upper(): #If I marry a charcter
			marry_enabled = False
			print("Married a character")
			return

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
			addRollToDatabase(character, False)

			if character in WishList:
				sleep(1)
				await message.add_reaction("⭐") #Marry the character


		if "Souhaité par" in message.content: #If message has a green bar (wish related)
			character = embed["author"]["name"]
			print("WISH : " + character)

			if not marry_enabled:
				return

			if "(Series)" in message.content:
				return

			await asyncio.gather(
			    AsyncWishMarry(message),
			    ContinuationOfFunction(message)
			)

			addCharacterToEmbedsStack((character, message))
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
		price = str(math.floor(int(price) * 1.7) + 1)  #The price on Tijimu's server is higher for some reason
		print(price)

		MudaeChannel = client.get_channel(863116140795396116)
		#await MudaeChannel.send("GaybenSay " + character + " : " + price) #Say the price of the character


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
					await queueMessage.add_reaction("⭐") #Marry the character



	if message.channel.id == 849723752065531945 and "**Gayben**," in message.content and not "**@Mudaebot**" in message.content: #If message is for timers
		message.content = message.content.replace(':', '.')
		message.content = message.content.replace('!', '.')
		timers = message.content.split(".")

		if "__" in timers[0]:
			marry_enabled = True
		else:
			marry_enabled = False

		marryReset = timers[1]
		marryReset = marryReset[marryReset.find("**") + 2:]
		marryReset = marryReset[:marryReset.find("**")]

		timerMarry.cancel()
		timerMarry = Timer(convertTimerToMinutes(marryReset)*60.0, enableMarry, ())
		timerMarry.start()

		kakeraReset = timers[4]

		if "$daily" in kakeraReset:
			kakeraReset = timers[5]

		if "__" in kakeraReset:
			kakera_grabber_enabled = True
		else:
			kakera_grabber_enabled = False

			kakeraReset = kakeraReset[kakeraReset.find("**") + 2:]
			kakeraReset = kakeraReset[:kakeraReset.find("**")]

			timerKakera.cancel()
			timerKakera = Timer(convertTimerToMinutes(kakeraReset)*60.0, enableKakeraGrabber, ())
			timerKakera.start()

		print("Timers : ")
		print("marry_enabled = " + str(marry_enabled))
		print("kakera_grabber_enabled = " + str(kakera_grabber_enabled))



		
@client.event
async def on_reaction_add(reaction, user): #Kakera grabber
	global kakera_grabber_enabled
	global KakeraList

	message = reaction.message

	if message.embeds != [] and (message.channel.id == 849723752065531945) and user.id == 432610292342587392: #If message has an embed, in the right channel and from mudae
		embed = message.embeds[0].to_dict()

		if not "color" in embed.keys():
			return

		color = embed["color"]
		if ("kakera".upper() in str(reaction).upper()): #If the reaction is about a kakera

			kakeraType = str(message.reactions[0]).upper()
			kakeraType = kakeraType[kakeraType.find(":") + 1:]
			kakeraType = kakeraType[:kakeraType.find(":")]

			if (kakera_grabber_enabled and (kakeraType in KakeraList)) or (kakeraType.upper() == "KakeraPPP".upper()):
				sleep(0.7)
				await message.add_reaction(message.reactions[0].emoji)
				kakera_grabber_enabled = False
				print("Grabbed a kakera (" + kakeraType + ")")

async def sayMessage(msg, delay):
	await asyncio.sleep(delay)
	print(msg)

async def AsyncWishMarry(msg):
	await asyncio.sleep(8.8)
	await msg.add_reaction("⭐")

async def ContinuationOfFunction(message):
	sleep(0.9)
	await message.add_reaction("⭐") #Marry the character

	user = client.get_user(242677066372218881)

	sleep(1)

	await message.remove_reaction("⭐", user)



def enableMarry():
	global marry_enabled
	marry_enabled = True

	print("Marry re-enabled")


def enableKakeraGrabber():
	global kakera_grabber_enabled
	kakera_grabber_enabled = True

	print("Kakera grabber re-enabled")


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

client.run("mfa.98AUeyEXxNdXmOW7gne82wWuJx7VuHItLO9vEyHgMxoHXd9c78p4j8PFmSFvC0dw4UQjJlQEe7zGcgVA_gbW")
