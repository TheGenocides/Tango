import aiosqlite
import difflib
import random
import animec

async def connect(filename):
	con=await aiosqlite.connect(filename)
	return con

async def cursor(con):
	cursor=await con.cursor()
	return cursor

async def find_user(condition):
	con=await connect("db/channel.db")
	cur=await cursor(con)
	await cur.execute("SELECT channel FROM channel WHERE member_id=?", (condition,))
	data=await cur.fetchone()
	await cur.close()
	await con.close()
	return True if data else False

async def find_videos(condition):
	con=await connect('db/video.db')
	cur=await cursor(con)
	
	await cur.execute("SELECT * FROM video")
	data=await cur.fetchall()
	alt_condition=condition[0] + condition[1] + condition[2]
	full_data=[(x[3], x[1], x[2], x[4], x[5], x[6], x[7], x[8], x[0], x[10], x[11], x[12]) for x in data if condition in x[1] or condition in x[1].split(" ") or condition.lower() in x[1] or condition.lower() in x[1].split(" ") or condition.upper() in x[1] or condition.upper() in x[1].split(" ") or condition in x[1].lower() or condition.lower() in x[1].lower() or alt_condition in x[1] or alt_condition.lower() in x[1] or alt_condition in x[1].lower() or alt_condition.lower() in  x[1].lower() or alt_condition in x[1][:3]]
	await cur.close()
	await con.close()
	return full_data

async def find_in_channel(condition,  *,mode="one"):
	con=await connect('db/channel.db')
	cur=await cursor(con)
	await cur.execute("SELECT * FROM channel WHERE member_id=?", (condition,))
	one=await cur.fetchone()
	all_=await cur.fetchall()

	await cur.close()
	await con.close()
	if mode.lower() == "one":
		return one

	elif mode.lower() == 'all':
		return all_

async def find_in_video(condition,  *,mode="one"):
	con=await connect('db/video.db')
	cur=await cursor(con)
	await cur.execute("SELECT * FROM video WHERE member_id=?", (condition,))
	
	if mode.lower() == "one":
		data=await cur.fetchone()
		await cur.close()
		await con.close()
		return data

	elif mode.lower() == 'all':
		data=await cur.fetchall()
		await cur.close()
		await con.close()
		return data

async def find_in_info(condition,  *,mode="one"):
	con=await connect('db/info.db')
	cur=await cursor(con)
	await cur.execute("SELECT * FROM info WHERE member_id=?", (condition,))
	one=await cur.fetchone()
	all_=await cur.fetchall()

	await cur.close()
	await con.close()
	if mode.lower() == "one":
		return one

	elif mode.lower() == 'all':
		return all_


def anime(name):
	anime = animec.Anime(name)
	data=(anime.name, anime.url, anime.description, anime.poster, anime.episodes, anime.aired, anime.teaser, random.choice(anime.opening_themes), random.choice(anime.ending_themes), anime.ranked, anime.genres, anime.type, anime.status, anime.rating, anime.popularity, anime.producers)
	return data
