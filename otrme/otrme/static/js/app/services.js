angular.module('services', [])
    .factory('RosterGetter', ['$http', function($http){
	return{
	    get: function(callback){
		$http.get('/roster/').success(function(data) {
		    // prepare data here
		    callback(data);
		});
	    }
	};
    }]);
