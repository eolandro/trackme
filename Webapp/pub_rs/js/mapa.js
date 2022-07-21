const mapa = {
	GO : 2,
	content : {},
	app : false,
	grptorres : [],
	trackmes : [],
	ready : 0,
	timeind : false,
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
		/////////////////////////////////////////////
		//setInterval(this.updateTrackme(),1000*20);
		/////////////////////////////////////////////
		this.timeind = Date.now();
		//this.timeind = 0;
		/////////////////////////////////////////////
		this.updateTrackme()
		/////////////////////////////////////////////
		this.app.ticker.add((delta) => this.gameLoop(delta));
	},
	gameLoop(delta) {
		
		let ahora = Date.now();
		let deltatime = ahora - this.timeind;
		if (deltatime > (1000*10)){
			console.log(ahora);
			this.updateTrackme();
			this.timeind = ahora;
			//////////////////////////////////////////
			for (var i = 0; i < this.trackmes.length; i++){
				let dispo = this.trackmes[i];
				////////////////////////////
				if (!this.trackmes[i]['gpt']){
					//this.app.stage.removeChild(this.trackmes[i]['gpt']);
					//////////////////////////////
					let cnt = new PIXI.Container();
					//////////////////////////////
					let gpt = new PIXI.Graphics();
					gpt.clear();
					gpt.lineStyle(3, 0xFEEB77, 1);
					gpt.beginFill(0x058400, 1);
					gpt.drawCircle(0, 0, 20);
					gpt.endFill();
					
					let txt = new PIXI.Text(
						this.trackmes[i]['MAC'],
						{
							fontFamily : 'Arial', 
							fontSize: 10, 
							fill : 0xFF0000, 
							align : 'center'
					});
					
					cnt.addChild(gpt);
					cnt.addChild(txt);
					
					this.app.stage.addChild(cnt);
					this.trackmes[i]['gpt'] = cnt;
				}
				////////////////////////////
				let x = 0;
				let y = 0;
				this.content['torres'].forEach( torre => {
					console.log(torre["id"],dispo["idTorre"]);
					if(torre["id"] == dispo["idTorre"]){
						console.log("Test");
						x = torre["pos"][0]; 
						y = torre["pos"][1];
						if (x < 360){
							x = x + Math.floor(Math.random() * 30);
							y = y + Math.floor(Math.random() * 30);
						}else{
							x = x - Math.floor(Math.random() * 30);
							y = y - Math.floor(Math.random() * 30);
						}
					}
					//////////////////////////////////////////////
					// mover contenedor
					if (this.trackmes[i]['visible']){
						this.trackmes[i]['gpt'].x = x;
						this.trackmes[i]['gpt'].y = y;
					}else{
						this.trackmes[i]['gpt'].x = 0;
						this.trackmes[i]['gpt'].y = 0;
					}
					//////////////////////////////////////////////
				});
				////////////////////////////
			}
			//////////////////////////////////////////
		}
	},
	updateTrackme(){
		///////////////////////////////////////////////////////
		var start = async () =>{
			var params = {
				method: 'POST', 
				headers: new Headers({
					'Content-Type': 'application/json'
				}),
				body: JSON.stringify({
					TKN: localStorage.TKN,
				})
			};
			
			response = await fetch('/api/obtenerTrackme',params)
			if (!response.ok)
				throw new Error("WARN", response.status)
			var R = response.json()
			return R
		};
		start().then( (Resp) => {
			console.log(Resp);
			if (Resp.R = 200){
				/////////////////////////
				for(var i = 0; i < this.trackmes.length; i++){
					this.trackmes[i]["visible"] = false;
				}
				/////////////////////////
				Resp.D.forEach( (valor) => {
					let vdata = {
							"idTorre" : valor[2],
							"MAC": valor[1],
							"gpt" : false,
							"visible": true
					};
					let encontrado = -1;
					for(var i = 0; i < this.trackmes.length; i++){
						if (this.trackmes[i]['MAC'] == vdata['MAC']){
							encontrado = i;
						}
					}
					if (encontrado == -1){
						this.trackmes.push(vdata);
					}else{
						this.trackmes[encontrado]["visible"] = true;
						this.trackmes[encontrado]["idTorre"] = vdata["idTorre"];
					}
				});
			}
		});
		///////////////////////////////////////////////////////
	}
}
///////////////////////////////////////////////////////
// Verificar la sesion
var verficar = async () =>{
	var params = {
		method: 'POST', 
		headers: new Headers({
			'Content-Type': 'application/json'
		}),
		body: JSON.stringify({
			TKN: localStorage.TKN
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

