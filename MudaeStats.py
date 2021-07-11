import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('mudae.db')
cursor = conn.cursor()
cursor.execute("""SELECT category, character, gender, price FROM roulette ORDER BY price ASC""")
rows = cursor.fetchall()

categories = [rows[i][0] for i in range(len(rows))]
characters = [rows[i][1] for i in range(len(rows))]
genders = [rows[i][2] for i in range(len(rows))]
prices = [rows[i][3] for i in range(len(rows))]

cursor.execute("""SELECT category, character, gender, price FROM roulette WHERE (category="Animanga roulette" OR category = "Game & Animanga") AND (gender = 2 OR gender = 3) ORDER BY price ASC""")
rows = cursor.fetchall()
prices_anime_women = [rows[i][3] for i in range(len(rows))]


cursor.execute("""SELECT category, character, gender, price FROM roulette WHERE (category="Animanga roulette" OR category = "Game & Animanga") AND (gender = 1 OR gender = 3) ORDER BY price ASC""")
rows = cursor.fetchall()
prices_anime_male = [rows[i][3] for i in range(len(rows))]


cursor.execute("""SELECT category, character, gender, price FROM roulette WHERE (category="Game roulette" OR category = "Game & Animanga") AND (gender = 2 OR gender = 3) ORDER BY price ASC""")
rows = cursor.fetchall()
prices_game_women = [rows[i][3] for i in range(len(rows))]


cursor.execute("""SELECT category, character, gender, price FROM roulette WHERE (category="Game roulette" OR category = "Game & Animanga") AND (gender = 1 OR gender = 3) ORDER BY price ASC""")
rows = cursor.fetchall()
prices_game_male = [rows[i][3] for i in range(len(rows))]



probability = [((len(prices) - i)/len(prices))*100 for i in range(len(prices))]
probability_anime_women = [((len(prices_anime_women) - i)/len(prices_anime_women))*100 for i in range(len(prices_anime_women))]
probability_anime_male = [((len(prices_anime_male) - i)/len(prices_anime_male))*100 for i in range(len(prices_anime_male))]
probability_game_women = [((len(prices_game_women) - i)/len(prices_game_women))*100 for i in range(len(prices_game_women))]
probability_game_male = [((len(prices_game_male) - i)/len(prices_game_male))*100 for i in range(len(prices_game_male))]

plt.subplot(111)

plt.title("Comparaison de la répartition des prix en kakera des personnages selon leur catégorie et sexe")
plt.plot(probability, prices, label = "Toutes catégories confondues", color="cyan")
plt.plot(probability_anime_women, prices_anime_women, label = "Personnage animé féminins", color="magenta")
plt.plot(probability_anime_male, prices_anime_male, label = "Personnage animé masculins", color="orangered")
plt.plot(probability_game_women, prices_game_women, label = "Personnage jeux vidéos féminins", color="darkviolet")
plt.plot(probability_game_male, prices_game_male, label = "Personnage jeux vidéos masculins", color="lightsalmon")

plt.xlabel("Top %")
plt.ylabel("Prix (kakera)")
plt.legend(loc="best")
plt.xlim(100,0)
plt.xticks([i for i in range(0, 100, 5)])
plt.grid()
plt.show()