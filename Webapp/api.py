from config import KEY # configuracion del servidor web
from pathlib import Path

def getToken():
	import uuid
	return { "R": 200 ,"D": str(uuid.uuid4()) }
	
async def authUser(DBO = None, TKN = None, USR = None, PWD = None ):
	if not DBO:
		return { "R":500 , "D": "Database"}
	if not TKN:
		return { "R":400 , "D": "Token"}
	if not USR:
		return { "R":400 , "D": "Usuario Contraseña"}
	if not PWD:
		return { "R":400 , "D": "Usuario Contraseña"}
	#################################################
	db = await DBO.getDB()
	#################################################
	
	# carga las clases y objetos necesarios
	import datetime
	import hashlib
	m = hashlib.sha256()
	m.update(bytes(PWD,encoding='utf8'))
	key = m.hexdigest()
	#########################
	## TODO verificar el id
	SQL = "select id from usuario where nombreacceso = ? and contrasena = ?"
	R = await db.execute(SQL,(USR,key))
	R = await R.fetchone()
	if R:
		usuario_id = R[0]
		SQL = "select id from acceso where usuario_id = ?"
		R = await db.execute(SQL,R)
		R = await R.fetchone()
		if not R:
			SQL = 'insert into acceso values(null,?,?,datetime(),0,"")'
			R = await db.execute(SQL,[TKN,usuario_id])
			await R.close()
		else:
			_id = R[0]
			SQL = f"update acceso set reject = 1 where id = {_id} "
			R = await db.execute(SQL)
			SQL = 'insert into acceso values(null,?,?,datetime(),0,"")'
			R = await db.execute(SQL,[TKN,usuario_id])
			
			await R.close()
		await db.commit()
		return { "R": 200 }
	return  { "R": 401, "D": "Usuario Contraseña" }
	
async def getidToken(DBO = None,TKN = None):
	#################################################
	db = await DBO.getDB()
	#################################################
	SQL = "select id from acceso where token = ? and reject = 0"
	R = await db.execute(SQL,[TKN])
	R = await R.fetchone()
	return R
	
async def checkToken(DBO = None,TKN = None):
	if not DBO:
		return { "R":500 , "D": "Database"}
	if not TKN:
		return { "R":400 , "D": "Token"}
		
	R = await getidToken(DBO,TKN)
	if not R:
		return {"R": 401}
	else:
		return { "R": 200 }
######################################################################
async def getidGateway(DBO = None,GWY = None):
	#################################################
	db = await DBO.getDB()
	#################################################
	SQL = "select id from gateway where token = ?"
	R = await db.execute(SQL,[GWY])
	R = await R.fetchone()
	return R
######################################################################
async def agregarDispositivo(DBO = None,TKN = None,NOM = None,MAC = None):
	if not DBO:
		return { "R":500 , "D": "Database"}
	if not TKN:
		return { "R":400 , "D": "Token"}
	if not NOM:
		return { "R":400 , "D": "Nombre"}
	if not MAC:
		return { "R":400 , "D": "Mac"}
	
	idusuario, = await getidToken(DBO,TKN)
	print(idusuario)
	
	#################################################
	db = await DBO.getDB()
	#################################################
	SQL = 'insert into dispositivo values(?,?,?)'
	R = await db.execute(SQL,[MAC.upper(),NOM,idusuario])
	print("=>",R.lastrowid)
	await R.close()
	await db.commit()
	return { "R": 200 }

######################################################################
async def obtenerTorres(DBO = None):
	#################################################
	db = await DBO.getDB()
	#################################################
	SQL = "select id,ubicacion from torre"
	R = await db.execute(SQL)
	D = await R.fetchall()
	await R.close()
	return { "R": 200, "D": D}
######################################################################
async def registrar(DBO = None,GWY = None,DSP = None,DAT = None):
	if not DBO:
		return { "R":500 , "D": "Database"}
	if not GWY:
		return { "R":400 , "D": "Gateway"}
	if not DSP:
		return { "R":400 , "D": "Mac"}
	"""
	if not DAT:
		return { "R":400 , "D": "Data"}
	"""
	#################################################
	db = await DBO.getDB()
	#################################################
	#################################################
	# Si el dispositivo esta registrado
	SQL = 'select macaddress from dispositivo where macaddress = ?'
	R = await db.execute(SQL,[DSP])
	if not R:
		return { "R":400 , "D": "RegMac"}
	#################################################
	# obtener el gateway
	idgateway, = await getidGateway(DBO,GWY)
	print("Gateway",idgateway)
	#################################################
	db = await DBO.getDB()
	#################################################
	# To-Do support for serveral towels
	SQL = 'select id from torre where gateway_id = ?'
	R = await db.execute(SQL,[idgateway])
	idtorre, = await R.fetchone()
	#################################################
	#################
	from datetime import datetime
	now = datetime.now()
	#################
	SQL = 'insert into entorres values(null,?,?,?)'
	R = await db.execute(SQL,[DSP.upper(),idtorre,now.isoformat()])
	print("entorres",R.lastrowid)
	#################
	if DAT:
		for dman in DAT:
			SQL = 'insert into cercatorres values(null,?,?,?,?)'
			R = await db.execute(SQL,[dman.upper(),DSP.upper(),idtorre,now.isoformat()])
			print("entorres",R.lastrowid)
	#await R.close()
	await db.commit()
	return { "R": 200 }
######################################################################
