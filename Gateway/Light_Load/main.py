from config import WEBSRV_DATA # configuracion del servidor web
from config import CLOUD_SERVER # url del servidor externo
from config import TOKEN # url del servidor externo
from fn import getMACfromIP
from flask import jsonify
from flask import Flask, request
from waitress import serve
import requests

app = Flask(__name__)

@app.route("/vecindario",methods=['POST'])
def vecindario():
	r_data = request.get_json()
	#######################################
	
	print(request.remote_addr)
	mac = getMACfromIP(request.remote_addr)
	if not mac:
		print('Auch')
		return r_data
	carga_Util = {
		"Token": TOKEN,
		"Dispositivo" :  mac,
		"Data": [r.replace(":","-").upper() for r in r_data] 
	}
	try:
		requests.post(CLOUD_SERVER, data = carga_Util)
	except Exception as err:
		pass
	else:
		print('Success!')
	print(r_data)
	return r_data
	
@app.route("/ping",methods=['GET'])
def ping():
	return jsonify(R = "pong")
	
	
serve(app, host = WEBSRV_DATA["HOST"], port = WEBSRV_DATA["PORT"])
