//No definida
if(typeof(localStorage.TKN) == "undefined"){
	window.location.href = "/";
}
//No string
if(typeof(localStorage.TKN) != "string" && trim(localStorage.TKN).length > 0 ){
	window.location.href = "/";
}
//No length
if( localStorage.TKN.trim().length == 0 ){
	window.location.href = "/";
}
