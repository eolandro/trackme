from sanic import Sanic
from sanic.response import json, html
from config import WEBSRV_DATA # configuracion del servidor web
from support import DBAccess # objeto de acceso a la base de datos

import dsapi # definiciones de funciones ocultas
import vapp # definiciones de funciones de las vistas
import api # definiciones de funciones de la api




app = Sanic(name="TrackMe")
app.config.RESPONSE_TIMEOUT = 360

DB = DBAccess()

#
#Elementos estaticos del servidor
#
app.static('/rs', './pub_rs')

#
# Vistas de la APP Front end
#

@app.route("/", methods=['GET'])
async def root(request):
	return html(vapp.login())

@app.route("/home", methods=['GET'])
async def home(request):
	return html(vapp.home())
	
@app.route("/mapa", methods=['GET'])
async def mapa(request):
	return html(vapp.mapa())
	
@app.route("/agregarDispositivo", methods=['GET'])
async def agregarDispositivo(request):
	return html(vapp.agregarDispositivo())

######################################################################
#
# Llamadas a los metodos de la api
#


######################################################################
#
# Dark Side of the Api
#

# Este metodo reconstruye la base de datos
# Solo es posible ejecutar este metodo si no hay base de datos

@app.route("/dsapi/db", methods=['GET'])
async def dsapi_DB(request):
	return json(await dsapi.database(DBO = DB))

########################################################################
@app.route("/api/getToken", methods=['GET'])
async def getToken(request):
	return json(api.getToken())
	
	
@app.route("/api/auth", methods=['POST'])
async def auth(request):
	return json(await api.authUser(
		DBO = DB,
		TKN = request.json['TKN'],
		USR = request.json['USR'],
		PWD = request.json['PWD']
	))
	
@app.route("/api/checkToken", methods=['POST'])
async def checkToken(request):
	if not 'TKN' in request.json:
		return json({"R":403})
	
	return json(await api.checkToken(
		DBO = DB,
		TKN = request.json['TKN']
	))
	
@app.route("/api/agregarDispositivo", methods=['POST'])
async def agregarDispositivo(request):
	if not 'TKN' in request.json:
		return json({"R":403})
	if not 'MAC' in request.json:
		return json({"R":400, "D":"Mac" })
	if not 'NOM' in request.json:
		return json({"R":400, "D":"Nombre" })
	
	return json(await api.agregarDispositivo(
		DBO = DB,
		TKN = request.json['TKN'],
		NOM = request.json['NOM'],
		MAC = request.json['MAC']
	))
	
@app.route("/api/registrar", methods=['POST'])
async def registrar(request):
	if not 'GWY' in request.json:
		return json({"R":403})
	if not 'DSP' in request.json:
		return json({"R":400, "D":"Mac" })
	DAT = None
	if 'DAT' in request.json:
		DAT = request.json['DAT']
	
	return json(await api.registrar(
		DBO = DB,
		GWY = request.json['GWY'],
		DSP = request.json['DSP'],
		DAT = DAT
	))
	
@app.route("/api/obtenerTorres", methods=['GET'])
async def obtenerTorres(request):
	return json(await api.obtenerTorres(DBO = DB))
	
if __name__ == "__main__":
    #app.run(host = WEBSRV_DATA["HOST"], port = WEBSRV_DATA["PORT"])
    app.run(host = WEBSRV_DATA["HOST"], port = WEBSRV_DATA["PORT"], dev=True, auto_reload=True)
