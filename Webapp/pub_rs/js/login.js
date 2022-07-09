window.app = new Vue({
	el: '#vuejs',
	data: {
		errorMsg: false,
		TKN: "",
		USR: "",
		PWD: ""
	},
	methods: {
		close: function(){
			this.errorMsg = false;
		},
		doLogin: function(){
			var start = async () =>{
				let response = await  fetch('/api/getToken')
				if (!response.ok)
					throw new Error("WARN", response.status)
				//////////////////////////////////
				var z = await response.json()
				this.TKN = z["D"];
				localStorage.TKN = this.TKN;
				
				var params = {
					method: 'POST', 
					headers: new Headers({
						'Content-Type': 'application/json'
					}),
					body: JSON.stringify({
						TKN: this.TKN,
						USR: this.USR,
						PWD: this.PWD
					})
				};
				
				response = await fetch('/api/auth',params)
				if (!response.ok)
					throw new Error("WARN", response.status)
				var R = response.json()
				return R
			};
			start().then( (Resp) => {
				console.log(Resp);
				switch(Resp.R){
					case 200:
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
		}
	}
});

