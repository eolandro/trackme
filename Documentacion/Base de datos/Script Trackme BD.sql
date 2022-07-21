BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "usuario" (
	"id"	INTEGER,
	"nombreacceso"	VARCHAR(45),
	"contrasena"	VARCHAR(256),
	"correo"	VARCHAR(256),
	"jsondata"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "gateway" (
	"id"	INTEGER,
	"token"	VARCHAR(128) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "torre" (
	"id"	INTEGER,
	"ubicacion"	VARCHAR(100) NOT NULL,
	"gateway_id"	INT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "acceso" (
	"id"	INTEGER,
	"token"	varchar(64) NOT NULL,
	"usuario_id"	INT NOT NULL,
	"login"	DATETIME NOT NULL,
	"reject"	INT NOT NULL,
	"jsondata"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "dispositivo" (
	"macaddress"	VARCHAR(16),
	"nombrecorto"	VARCHAR(45),
	"usuario_id"	INT,
	PRIMARY KEY("macaddress")
);
CREATE TABLE IF NOT EXISTS "entorres" (
	"id"	INTEGER,
	"dispositivo_mac"	VARCHAR(16) NOT NULL,
	"torre_id"	INT NOT NULL,
	"fechahora"	DATETIME NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "cercatorres" (
	"id"	INTEGER,
	"dispositivo_mac"	VARCHAR(16) NOT NULL,
	"dispositivo_ref"	VARCHAR(16) NOT NULL,
	"torre_id"	INT NOT NULL,
	"fechahora"	DATETIME NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "usuario" ("id","nombreacceso","contrasena","correo","jsondata") VALUES (1,'super','73d1b1b1bc1dabfb97f216d897b7968e44b06457920f00f2dc6c1ed3be25ad4c','super@super.com','""');
INSERT INTO "gateway" ("id","token") VALUES (1,'2a12640dfaf100dff963464aff6adcc08c5e513e86e04862db95cc439f87d2a3');
INSERT INTO "gateway" ("id","token") VALUES (1,'03aed8f78eac7a6029c5f0a1e15368104c6e9470c3849521c876e1b70ab0bf3e');
INSERT INTO "torre" ("id","ubicacion","gateway_id") VALUES (1,'180,240',1);
INSERT INTO "torre" ("id","ubicacion","gateway_id") VALUES (2,'595,240',1);
COMMIT;
