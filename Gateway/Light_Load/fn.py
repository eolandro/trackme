import pathlib
from config import LEASES_FILE

def getMACfromIP(ip):
	lf = open(LEASES_FILE)
	if lf.exists():
		for lease in lf.open():
			# 1657127373 8c:f1:12:f8:a8:64 192.168.96.92 * 01:8c:f1:12:f8:a8:64
			fila = lease.strip().split(" ")
			if fila[-3] == ip:
				return fila[-1].replace(":","-").upper()
	return False
