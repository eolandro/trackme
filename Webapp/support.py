import asyncio
import aiosqlite
from config import DB_DATA
class DBAccess:
	def __init__(self):
		self.DB = None
	async def getDB(self):
		if not self.DB:
			self.DB = await aiosqlite.connect(
				DB_DATA['DBURL'], 
				#MONGOD_DATA['PORT'],
				loop=asyncio.get_event_loop()
			)
		return self.DB
