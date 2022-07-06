from pathlib import Path
from config import LEASES_FILE

def getMACfromIP(ip):
	lf = Path(LEASES_FILE)
	if lf.exists():
		for lease in lf.open():
			#            A8E81E3D4C08
			#            91751aec9ac7
			#            91:75:1a:ec:9a:c7
			# 1657127373 8c:f1:12:f8:a8:64 192.168.96.92 * 01:8c:f1:12:f8:a8:64
			fila = lease.strip().split(" ")
			print(fila)
			if fila[-3] == ip:
				return fila[1].replace("-","").replace(":","").upper()
	return False
