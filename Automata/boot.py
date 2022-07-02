# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
"""
	Nuestro boot debe esperar alrededor de 20 segundos, para arracar
	a main, esto con el objetivo de que si algo falla, podamos parar
	la secuencia de arranque

"""
import time

max_tiempo = 20
segundos = 0
inicio = time.ticks_ms()
parar = False
while not parar:
	# Computamos la diferencia de tiempo
	delta = time.ticks_diff(time.ticks_ms(), inicio) 
	if delta > 1000:
		segundos = segundos + 1
		print(segundos)
		inicio = time.ticks_ms()
	if segundos >= max_tiempo:
		parar = True
############################
print("Ejecutando Main")
import main
main.run()
