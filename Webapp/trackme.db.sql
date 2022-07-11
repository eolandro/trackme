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
INSERT INTO "torre" ("id","ubicacion","gateway_id") VALUES (1,'180,240',1);
INSERT INTO "torre" ("id","ubicacion","gateway_id") VALUES (2,'595,240',1);
INSERT INTO "acceso" ("id","token","usuario_id","login","reject","jsondata") VALUES (1,'db74757d-7f56-4956-a9d9-07b4186ea24c',1,'2022-07-08 18:38:17',1,'');
INSERT INTO "acceso" ("id","token","usuario_id","login","reject","jsondata") VALUES (2,'595e0a80-bc57-4eae-8481-0d57828f038f',1,'2022-07-09 16:22:48',0,'');
INSERT INTO "acceso" ("id","token","usuario_id","login","reject","jsondata") VALUES (3,'4d32e1f1-b387-47cd-9073-ca8d63755c01',1,'2022-07-09 17:37:02',0,'');
INSERT INTO "acceso" ("id","token","usuario_id","login","reject","jsondata") VALUES (4,'95001524-fbb9-4d0d-9adb-002d3323465d',1,'2022-07-11 17:37:26',0,'');
INSERT INTO "dispositivo" ("macaddress","nombrecorto","usuario_id") VALUES ('E0D55E48C0BA','leopc',1);
INSERT INTO "entorres" ("id","dispositivo_mac","torre_id","fechahora") VALUES (1,'E0D55E48C0BA',1,'2022-07-08T20:17:34.870663');
COMMIT;
