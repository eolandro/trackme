from config import WEBSRV_DATA # configuracion del servidor web
from config import CLOUD_SERVER # url del servidor externo
from config import TOKEN # url del servidor externo
from fn import getMACfromIP
from flask import jsonify
from flask import Flask, request
from flask import json
from waitress import serve
import requests

app = Flask(__name__)

# este metodo se agrega cuando un dispositivo de conecta 
# al gateway
@app.route("/vecindario",methods=['POST'])
def vecindario():
	r_data = request.get_json()
	#######################################
	print(request.remote_addr)
	mac = getMACfromIP(request.remote_addr)
	print(mac)
	if not mac:
		print('Auch')
		return jsonify(R = "Auch")
	carga_Util = {
		"GWY": TOKEN,
		"DSP" :  mac,
		"DAT": [r.upper() for r in r_data] 
	}
	print(carga_Util)
	try:
		R = requests.post(
			CLOUD_SERVER + "/api/registrar", 
			headers = {'content-type': 'application/json'}, 
			data = json.dumps(carga_Util)
		)
		print(R.content)
	except Exception as err:
		pass
	else:
		print('Success!')
	
	return jsonify(R = "ok")

# Este metodo se ejecuta para mantener al gateway
@app.route("/ping",methods=['GET'])
def ping():
	print(request.remote_addr)
	mac = getMACfromIP(request.remote_addr)
	print(mac)
	if not mac:
		print('Auch')
		return jsonify(R = "Auch")
	carga_Util = {
		"GWY": TOKEN,
		"DSP" :  mac,
	}
	print(carga_Util)
	#######################################
	try:
		R = requests.post(
			CLOUD_SERVER + "/api/actualizar",
			headers = {'content-type': 'application/json'}, 
			data = json.dumps(carga_Util)
		)
		print(R.content)
	except Exception as err:
		pass
	else:
		print('Success!')
	#######################################
	return jsonify(R = "pong")
	
	
serve(app, host = WEBSRV_DATA["HOST"], port = WEBSRV_DATA["PORT"])
