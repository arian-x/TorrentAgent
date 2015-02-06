// (function(){
// })();
(function(){


	var app = angular.module('torrent_agent',[]) //the array is for the dependencies
	app.controller("InputController",['$http',function($http){
		  this.download_torrent = function(magnet){
			//console.log("magnet")
			$http.get('/download?mag='+magnet,{'mag':magnet}).success(function(data){
				console.log("magnet is :"+data)
			})
		}
	}]);
})();

