import sys
import datetime

fromiso = None
fromisodot = None


def getisoformat(S):
	if not S:
		return S
	DT = S.split('T')
	if (len(DT) > 1):
		T = DT[1]
		if '.' in T:
			return "%Y-%m-%dT%H:%M:%S.%f"
		else:
			return "%Y-%m-%dT%H:%M:%S"
	else:
		return "%Y-%m-%d"
		

def ffromiso(d):
	F = getisoformat(d)
	return datetime.datetime.strptime(d, F)

if sys.version_info >= (3,7,0):
	fromiso = datetime.datetime.fromisoformat
else:
	#fromiso = lambda d : datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S")
	fromiso = ffromiso
	
if sys.version_info >= (3,7,0):
	fromisodot = datetime.datetime.fromisoformat
else:
	#fromisodot = lambda d : datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f")
	fromisodot = ffromiso
