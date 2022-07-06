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
		("Pi3-AP","pimylifeup")
	],
	"APDescubiertos" : [],
	"Estado" : 0,
	"Simbolo" : "",
	"Server" : "http://api.trackme",
	"Puerto" : "8000",
	"MetodoEntrega" : "vecindario",
	"MetodoPing" : "ping",
	"WLAN" : None
}

def inicial():
	print("Inicial")
	DatosAutomata["Estado"] = 1
	DatosAutomata["Simbolo"] = "Listo"
	
def buscando():
	print("Buscando")
	#Colocando en modo estacion
	DatosAutomata['WLAN'] = network.WLAN(network.STA_IF) # create station interface
	DatosAutomata['WLAN'].active(True)	   # activate the interface
	lAPSSID = []
	##################################################################
	# Escaneo de las redes inalambrcas
	# 5 Intentos separados por 10 segundos
	##################################################################
	for intentos in range(5):
		for a in DatosAutomata['WLAN'].scan(): # scan for access points
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
			if not DatosAutomata['WLAN'].isconnected():
				print('connecting to network...',Cred[0])
				DatosAutomata['WLAN'].connect(Cred[0], Cred[1])
				start = time.ticks_ms() # get millisecond counter
				Segundos  = 0
				while Segundos < 21:
					resp = DatosAutomata['WLAN'].isconnected()
					if resp:
						Segundos = 21
					delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
					if delta > 1000:
						Segundos = Segundos + 1
						start = time.ticks_ms()
				if DatosAutomata['WLAN'].isconnected():
						print('network config:', DatosAutomata['WLAN'].ifconfig())
						DatosAutomata["Estado"] = 2
						DatosAutomata["Simbolo"] = "Conectado"
						return
			# Pudo haber un problema con el gateway si esta nuevamente disponible
		###################
		print("Esperando",intentos)
		Segundos  = 0
		start = time.ticks_ms() # get millisecond counter
		while Segundos < 9:
			delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
			if delta > 1000:
				print("S",Segundos)
				Segundos = Segundos + 1
				start = time.ticks_ms()
	#####################################################
	DatosAutomata["Estado"] = 3
	DatosAutomata["Simbolo"] = "No Conectado"

def anclado():
	print("Anclado")
	if DatosAutomata['APDescubiertos']:
		Enviado = None
		# Enviando la lista de APDescubiertos
		try:
			print('Enviando POST')
			post_data = json.dumps(DatosAutomata['APDescubiertos'])
			request_url = DatosAutomata['Server']+':'+DatosAutomata['Puerto']+'/'+ DatosAutomata['MetodoEntrega']
			print(request_url,post_data)
			R = urequests.post(request_url, headers = {'content-type': 'application/json'}, data = post_data)
			print("Retorno",R.content)
			Enviado = True
		except OSError as err:
			print(err)
			print("EVecindario")
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
				request_url = DatosAutomata['Server']+':'+DatosAutomata['Puerto']+'/' + DatosAutomata['MetodoPing']
				print(request_url)
				R = urequests.get(request_url)
				print("Retorno",R.content)
			except OSError as err:
				print(err)
				Conexion_Perdida = True
		delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
		if delta > 1000:
			print("S",Segundos)
			Segundos = Segundos + 1
			start = time.ticks_ms()
	
	DatosAutomata["Estado"] = 3
	DatosAutomata["Simbolo"] = "No Conectado"

def visible():
	print("Visible")
	# Realizamos la desconexion de la red
	DatosAutomata['WLAN'].disconnect()
	# Visisble por 5 segundos
	Segundos  = 0
	start = time.ticks_ms() # get millisecond counter
	while Segundos < 5:
		delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
		if delta > 1000:
			print("S",Segundos)
			Segundos = Segundos + 1
			start = time.ticks_ms()
	########################################
	ap = network.WLAN(network.AP_IF) # create access-point interface
	#ap.config(ssid='TRCKME') # Esto deberia colocar el SSID pero parece no estar disponible
	#ap.config(max_clients=1) # Esto deberia colocar cuantos clientes pero parece no estar disponible
	ap.active(True)		 # activate the interface
	# Visisble por 15 segundos
	Segundos  = 0
	start = time.ticks_ms() # get millisecond counter
	while Segundos < 15:
		delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
		if delta > 1000:
			print("S",Segundos)
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
			buscando()
		if DatosAutomata["Estado"] == 2:
			anclado()
		if DatosAutomata["Estado"] == 3:
			visible()
