// (function(){
// })();
var socket = io.connect("http://"+document.domain+":"+location.port+'/test');
var numbers_received = [];
socket.on('newnumber',function(msg){
	//alert("yohooo");
	console.log("Received number: "+msg.number);
});
socket.on('newinfo',function(msg){
	//alert("yohooo");
	console.log("Received info: "+msg.info);
});
var app = angular.module('torrent_agent',[]); //the array is for the dependencies
app.controller("InputController",['$http',function($http){
	
	//socket.on('my response',function(msg){
	//	console.log(msg.data);
	//});

	this.download_torrent = function(magnet){
			//socket.emit('my event',{data:magnet});
		  	$http.get('/download?mag='+magnet,{'mag':magnet}).success(function(data){
		  		console.log("magnet is :"+data);
		  	})
	}
}]);

