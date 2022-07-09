from config import KEY # configuracion del servidor web

async def database(DBO = None):
	if not DBO:
		return False	
	db = await DBO.getDB()
	SQL = """
	CREATE TABLE IF NOT EXISTS usuario (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nombreacceso VARCHAR(45) NULL,
	contrasena VARCHAR(256) NULL,
	correo VARCHAR(256) NULL,
	jsondata TEXT NOT NULL
	);
	
	CREATE TABLE IF NOT EXISTS "acceso" (
	"id"	INTEGER,
	"usuario_id"	INT NOT NULL,
	"login"	DATETIME NOT NULL,
	"reject"	INT NOT NULL,
	"jsondata"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
	);
	
	CREATE TABLE IF NOT EXISTS dispositivo (
	macaddress VARCHAR(16) PRIMARY KEY,
	usuario_id INT NULL
	);
	
	CREATE TABLE IF NOT EXISTS gateway (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	token VARCHAR(128) NOT NULL
	);
	
	
	CREATE TABLE IF NOT EXISTS torre (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	ubicacion VARCHAR(100) NOT NULL,
	gateway_id INT NOT NULL
	);
	
	CREATE TABLE IF NOT EXISTS registro (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	dispositivo_macadd VARCHAR(16) NOT NULL,
	dispositivo_macref VARCHAR(16) NOT NULL,
	fechahora DATETIME NOT NULL
	);
	
	INSERT INTO "usuario" ("id","nombreacceso","contrasena","correo","jsondata") VALUES (1,'super','73d1b1b1bc1dabfb97f216d897b7968e44b06457920f00f2dc6c1ed3be25ad4c','super@super.com','""');
	"""
	#await db.execute(SQL.strip())
	await db.executescript(SQL.strip())
	return { "R": 200 }

