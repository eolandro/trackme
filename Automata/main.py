"""
Este es el codigo principal para el ESP32

Previamente es necesario instalar urequests
en la REPL de micropython instalar
import upip
upip.install("micropython-urequests")

"""
import network
import binascii
import time
import urequests
import json

DatosAutomata = {
	"APConectar" : [
		("IZZI-A7A6","64UCqtcRHQBq")
	],
	"APDescubiertos" : [],
	"Estado" : 0,
	"Simbolo" : "",
	"Server" : "http://api.trackme",
	"Puerto" : "8080",
	"MetodoEntrega" : "vecindario",
	"MetodoPing" : "ping"
}

def inicial():
	DatosAutomata["Estado"] = 1
	DatosAutomata["Simbolo"] = "Listo"
	
def buscando():
	#Colocando en modo estacion
	wlan = network.WLAN(network.STA_IF) # create station interface
	wlan.active(True)	   # activate the interface
	lAPSSID = []
	##################################################################
	# Escaneo de las redes inalambrcas
	# 5 Intentos separados por 10 segundos
	##################################################################
	for intentos in range(5):
		for a in wlan.scan(): # scan for access points
			ssid = a[0].decode()
			bssid = binascii.hexlify(a[1]).decode()
			
			if not ssid in lAPSSID:
				lAPSSID.append(ssid)
			if len( DatosAutomata['APDescubiertos']) < 15:
				if not bssid in DatosAutomata['APDescubiertos']:
					DatosAutomata['APDescubiertos'].append(bssid)
		# credenciales
		Cred = None
		
		for ap in DatosAutomata['APConectar']:
			if ap[0] in lAPSSID:
				Cred = ap
		# Intentamos conectarnos
		if Cred:
			if not wlan.isconnected():
				print('connecting to network...',Cred[0])
				wlan.connect(Cred[0], Cred[1])
				start = time.ticks_ms() # get millisecond counter
				Segundos  = 0
				while Segundos < 21:
					resp = wlan.isconnected()
					if resp:
						Segundos = 21
					delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
					if delta > 1000:
						Segundos = Segundos + 1
						start = time.ticks_ms()
				if wlan.isconnected():
						print('network config:', wlan.ifconfig())
						DatosAutomata["Estado"] = 2
						DatosAutomata["Simbolo"] = "Conectado"
						return
		###################
		Segundos  = 0
		start = time.ticks_ms() # get millisecond counter
		while Segundos < 9:
			delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
			if delta > 1000:
				Segundos = Segundos + 1
				start = time.ticks_ms()
	#####################################################
	DatosAutomata["Estado"] = 3
	DatosAutomata["Simbolo"] = "No Conectado"

def anclado():
	if DatosAutomata['APDescubiertos']:
		Enviado = None
		# Enviando la lista de APDescubiertos
		try:
			post_data = ujson.dumps(DatosAutomata['APDescubiertos'])
			request_url = DatosAutomata['Server']+':'+DatosAutomata['Puerto']+'/'+ DatosAutomata['MetodoEntrega']
			requests.post(request_url, headers = {'content-type': 'application/json'}, data = post_data)
			Enviado = True
		except:
			Enviado = False
	
	if Enviado:
		while DatosAutomata['APDescubiertos']:
			DatosAutomata['APDescubiertos'].pop()
	
	# etapa de ping
	start = time.ticks_ms() # get millisecond counter
	Segundos  = 0
	Conexion_Perdida = False
	while not Conexion_Perdida:
		if Segundos > 4:
			Segundos = 0
			try: # Realizando el ping al servidor
				requests.get(DatosAutomata['Server']+':'+DatosAutomata['Puerto']+'/' + DatosAutomata['MetodoPing'])
			except:
				Conexion_Perdida = True
		delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
		if delta > 1000:
			Segundos = Segundos + 1
			start = time.ticks_ms()
	
	DatosAutomata["Estado"] = 3
	DatosAutomata["Simbolo"] = "No Conectado"

def visible():
	ap = network.WLAN(network.AP_IF) # create access-point interface
	ap.config(ssid='TRCKME') # set the SSID of the access point
	ap.config(max_clients=1) # set how many clients can connect to the network
	ap.active(True)		 # activate the interface
	# Visisble por 15 segundos
	Segundos  = 0
	start = time.ticks_ms() # get millisecond counter
	while Segundos < 15:
		delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
		if delta > 1000:
			Segundos = Segundos + 1
			start = time.ticks_ms()
	##########################################
	DatosAutomata["Estado"] = 1
	DatosAutomata["Simbolo"] = "Listo"
	
def run():
	while True:
		if DatosAutomata["Estado"] == 0:
			inicial()
		if DatosAutomata["Estado"] == 1:
			inicial()
