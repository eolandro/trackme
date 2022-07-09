from jinja2 import Environment, FileSystemLoader, select_autoescape
from config import BULMA_URL,VUEJS_URL,PIXIJ_URL

env = Environment(
    loader = FileSystemLoader('./templates'),
    autoescape = select_autoescape(['html','xml','tmpl'])
)

def cargarVista(t_template, title ,lcss, ljs, atras = False):
	if not t_template:
		return False
	if not title:
		return False
	if not lcss:
		return False
	if not ljs:
		return False
		
	if not isinstance(t_template,str):
		return False
	if not isinstance(title,str):
		return False
	if not isinstance(lcss,list):
		return False
	if not isinstance(ljs,list):
		return False
		
	template = None
	render = None
	try:
		template = env.get_template(t_template)
		if atras:
			render = template.render(t_title = title,l_css = lcss,l_js = ljs, l_atras = atras)
		else:
			render = template.render(t_title = title,l_css = lcss,l_js = ljs)
	except:
		import sys
		print("Oops!",sys.exc_info()[0],"occured.")
		template = env.get_template('almacen/error.html.tmpl')
		render = template.render(
		t_title = 'Como?',		
		l_css = [
			BULMA_URL,
			"/rs/css/base.css"
		],
		l_js = [
			VUEJS_URL,
			"/rs/js/login.js"
		])
	return render

def login():
	return cargarVista('login.html.tmpl',"Menu",
		[BULMA_URL,"/rs/css/base.css"],
		[VUEJS_URL,"/rs/js/login.js"]
	)
	
def home():
	return cargarVista('home.html.tmpl',"Menu",
		[BULMA_URL,"/rs/css/base.css"],
		[VUEJS_URL,'/rs/js/base.js']
	)
	
def mapa():
	return cargarVista('mapa.html.tmpl',"Mapa",
		[BULMA_URL,"/rs/css/base.css"],
		[PIXIJ_URL,'/rs/js/base.js','/rs/js/mapa.js'],
		"home"
	)
	
def agregarDispositivo():
	return cargarVista('agregarDispositivo.html.tmpl',"Agregar Dispositivo",
		[BULMA_URL,"/rs/css/base.css"],
		[VUEJS_URL,'/rs/js/base.js','/rs/js/agregardispositivo.js'],
		"home"
	)
