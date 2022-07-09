window.app = new Vue({
	el: '#vuedispositivo',
	data: {
		errorMsg: false,
		disabled: false,
		txtnom: "",
		txtmac: "",
		TKN: localStorage.TKN
	},
	methods: {
		close: function(){
			this.errorMsg = false;
		},
		verificar:() => {
			this.TKN = localStorage.TKN;
			var start = async () =>{
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
			start().then( (Resp) => {
				console.log(Resp);
				if (Resp.R == 403){
					window.location.href = '/';
				}
			});
		},
		doOk: function(){
			window.app.verificar();
			console.log(this.txtnom);
			if (!window.app.txtnom){
				alert("Por favor ingrese un valor a nombre");
				return;
			}
			if (!window.app.txtmac){
				alert("Por favor ingrese un valor a la mac");
				return;
			}
			window.app.txtmac = window.app.txtmac.trim();
			if (window.app.txtmac.length != 12){
				alert("Por favor, revise la mac no cumple con el formato");
				return;
			}
			var r = window.app.txtmac.match(/[0-9A-Fa-f]{12}$/g);
			
			if (r.length != 1){
				alert("Por favor ingrese una mac valida");
				return;
			}///[0-9A-Fa-f]{6}/g
			var start = async () =>{
				this.TKN = localStorage.TKN;
				var params = {
					method: 'POST', 
					headers: new Headers({
						'Content-Type': 'application/json'
					}),
					body: JSON.stringify({
						TKN: this.TKN,
						NOM: this.txtnom,
						MAC: this.txtmac,
					})
				};
				
				response = await fetch('/api/agregarDispositivo',params)
				if (!response.ok)
					throw new Error("WARN", response.status)
				var R = response.json()
				return R
			};
			start().then( (Resp) => {
				console.log(Resp);
				switch(Resp.R){
					case 200:
						alert("Cuardado");
						window.location.href = '/home';
						//console.log("Yei!!");
					break;
					case 401:
						alert("El usuario no Existe o la contraseña no es valida");
					break;
					case 406:
						alert("Usuario o contraseña vácios");
					break;
					case 500:
						alert("Fallo interno favor de comunicar con desarrollo");
					break;
				}
			});
		},
		guardarSalida: function(){
			
		},
		cancelar: function(){
			window.location.href = '/home';
		}
	},
	computed:{
		isDisabled(){
			return this.disabled;
		}
	}
});

