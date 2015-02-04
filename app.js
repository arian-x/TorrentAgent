// (function(){
// })();
(function(){


	var app = angular.module('torrent_agent',[]) //the array is for the dependencies
	app.controller("InputController",function(){
		this.download_torrent = function(magnet){
			console.log("magnet")
		}
	});
})();

