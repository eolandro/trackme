const mapa = {
	GO : 2,
	content : {},
	app : false,
	grptorres : [],
	ready : 0,
	canStart(){
		if (this.ready == this.GO){
			this.inicialize();
		}
	},
	inicialize(){
		let app = new PIXI.Application({ width: 720, height: 480 });
		app.stage.interactive = true;
		let pixijs = document.getElementById("pixijs");
		app.renderer.backgroundColor = 0xF5F6F7;
		pixijs.appendChild(app.view);
		this.app = app;
		this.setup();
	},
	setup(){
		console.log("Ready");
		/////////////////////////
		// Creamos el Edificio
		const Edificio = new PIXI.Graphics();
		let ix = this.content['edificio'][0][0];
		let iy = this.content['edificio'][0][1];
		Edificio.lineStyle(4, 0x00d1b2, 1);
		Edificio.beginFill(0xeeeeee, 0.25);
		Edificio.moveTo(ix, iy);
		this.content['edificio'].forEach( punto => {
			Edificio.lineTo(punto[0],punto[1]);
		});
		Edificio.closePath();
		Edificio.endFill();
		this.app.stage.addChild(Edificio);
		/////////////////////////
		// Creamos las torres
		this.content['torres'].forEach( torre => {
			let gpt = new PIXI.Graphics();
			// Circle + line style 1
			gpt.lineStyle(2, 0xFEEB77, 1);
			gpt.beginFill(0x650A5A, 0.25);
			gpt.drawCircle(torre["pos"][0], torre["pos"][1], 120);
			gpt.endFill();
			this.app.stage.addChild(gpt);
			this.grptorres.push(gpt);
		});
	}
}
///////////////////////////////////////////////////////
// Verificar la sesion
this.TKN = localStorage.TKN;
var verficar = async () =>{
	var params = {
		method: 'POST', 
		headers: new Headers({
			'Content-Type': 'application/json'
		}),
		body: JSON.stringify({
			TKN: this.TKN
		})
	};
	
	response = await fetch('/api/checkToken',params)
	if (!response.ok)
		throw new Error("WARN", response.status)
	var R = response.json()
	return R
};
///////////////////////////////////////////////////////
// Cargar las torres

var cargarTorres = async () =>{
	response = await fetch('/api/obtenerTorres')
	if (!response.ok)
		throw new Error("WARN", response.status)
	var R = response.json()
	return R
};
///////////////////////////////////////////////////////
async function procesarTorres(Resp){
	if (Resp.R == 200){
		mapa.content["torres"] = [];
		Resp.D.forEach( (t)  => { 
			let xys = t[1].split(",");
			x = parseFloat((xys[0]));
			y = parseFloat((xys[1]));
			
			mapa.content["torres"].push({
				"id" : t[0],
				"pos": [x,y]
			});
		});
		mapa.ready++;
		mapa.canStart();
	}
}
///////////////////////////////////////////////////////
///////////////////////////////////////////////////////
//Cargar el mapa
var cargarMapa = async () =>{
	response = await fetch('/rs/json/mapa.json')
	if (!response.ok)
		throw new Error("WARN", response.status)
	var R = response.json()
	return R
};
async function procesarMapa(Resp){
	mapa.content = Resp;
	// Ejecutanmos la primera etapa
	mapa.ready++;
	mapa.canStart();
	//Ejecutarmos la segunda etapa
	cargarTorres().then(procesarTorres);
}
///////////////////////////////////////////////////////
verficar().then( (Resp) => {
	console.log(Resp);
	if (Resp.R == 403){
		window.location.href = '/';
	}
	////////////////////////////////////
	if (Resp.R == 200){
		//mapa.inicialize()
		cargarMapa().then(procesarMapa);
		
		
	}
	////////////////////////////////////
});
///////////////////////////////////////////////////////

