import aiosqlite
import difflib
import random
import animec
import time
from uuid import uuid4

async def connect(filename):
	con=await aiosqlite.connect(filename)
	return con

async def cursor(con):
	cursor=await con.cursor()
	return cursor

async def is_video(id):
	con=await connect("db/video.db")
	cur=await cursor(con)
	await cur.execute("SELECT * FROM video WHERE ID = ?", (id,))
	data=await cur.fetchone()
	await cur.close()
	await con.close()
	return True if data else False

async def find_user(condition):
	con=await connect("db/channel.db")
	cur=await cursor(con)
	await cur.execute("SELECT channel FROM channel WHERE member_id=?", (condition,))
	data=await cur.fetchone()
	await cur.close()
	await con.close()
	return True if data else False

async def view(id):
	con=await connect('db/video.db')
	cur=await cursor(con)
	
	await cur.execute("SELECT * FROM video WHERE ID = ?", (id,))
	data=await cur.fetchall()

	full_data=[(x[3], x[1], x[2], x[4], x[5], x[6], x[7], x[8], x[0], x[10], x[11], x[12], x[14], x[15]) for x in data]
	await cur.close()
	await con.close()
	return full_data

async def find_videos(condition):
	con=await connect('db/video.db')
	cur=await cursor(con)
	
	await cur.execute("SELECT * FROM video WHERE deleted = ? AND verified = ?", ("n", "y"))
	data=await cur.fetchall()
	alt_condition=condition[0] + condition[1] + condition[2]
	full_data=[(x[3], x[1], x[2], x[4], x[5], x[6], x[7], x[8], x[0], x[10], x[11], x[12], x[14], x[15]) for x in data if condition in x[1] or condition in x[1].split(" ") or condition.lower() in x[1] or condition.lower() in x[1].split(" ") or condition.upper() in x[1] or condition.upper() in x[1].split(" ") or condition in x[1].lower() or condition.lower() in x[1].lower() or alt_condition in x[1] or alt_condition.lower() in x[1] or alt_condition in x[1].lower() or alt_condition.lower() in  x[1].lower() or alt_condition in x[1][:3]]
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

async def find_in_video(condition,  deleted:bool, *,mode="one"):
	deleted='y' if deleted else 'n'
	con=await connect('db/video.db')
	cur=await cursor(con)
	await cur.execute("SELECT * FROM video WHERE member_id = ? AND deleted = ?", (condition, deleted))
	
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

async def comments(bot, commenter_id: int, video_id: int, content: str):
	await bot.wait_until_ready()
	comment_id=str(uuid4().int)[:10]
	con=await connect('db/comment.db')
	cur=await cursor(con)
	await cur.execute("CREATE TABLE IF NOT EXISTS comments(commenter_id int, video_id int, content text, comment_id, date)")
	try:
		_date=int(time.time())
		await cur.execute("INSERT OR IGNORE INTO comments(commenter_id, video_id, content, comment_id, date) VALUES (?,?,?,?,?)", (commenter_id, video_id, content, comment_id, _date))
		await con.commit()

		await cur.close()
		await con.close()

		con=await connect("db/video.db")
		cur=await cursor(con)
		await cur.execute("UPDATE video SET comments = comments + 1 WHERE ID = ?", (video_id,))
		
		await con.commit()
		await cur.close()
		await con.close()

	except Exception as e:
		raise e 

async def is_nsfw(ID):
	con=await connect("db/video.db")
	cur=await cursor(con)

	await cur.execute("SELECT nsfw FROM video WHERE ID = ?", (ID,))
	nsfw=await cur.fetchone()

	return True if nsfw == 'y' else False 

async def find_in_video_by_id(ID,  deleted:bool, *,mode="one"):
	deleted='y' if deleted else 'n'
	con=await connect('db/video.db')
	cur=await cursor(con)
	await cur.execute("SELECT * FROM video WHERE ID = ? AND deleted = ?", (ID, deleted))
	
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

async def get_channel_name(id):
	data=await find_in_channel(id)
	return data[1]

def anime(name):
	anime = animec.Anime(name)
	data=(anime.name, anime.url, anime.description, anime.poster, anime.episodes, anime.aired, anime.teaser, random.choice(anime.opening_themes), random.choice(anime.ending_themes), anime.ranked, anime.genres, anime.type, anime.status, anime.rating, anime.popularity, anime.producers, anime.is_nsfw())
	return data

def lyric(name):
	lyric=animec.Anilyrics(name)
	return (lyric.url, lyric.english(), lyric.romaji(), lyric.kanji())