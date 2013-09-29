angular.module('services', [])
    .factory('OtrmeApi', ['$http', function($http) {
	var d = {};
	d['get_roster'] = function(callback) {
		$http.get('/roster/').success(function(data) {
		    // data should be a list of user info objects
		    // see get_user_info
		    callback(data);
		});
	};

	d['get_user_info'] = function(channel, callback) {
	    $http.get('/roster/' + channel).success(function(data) {
		/* data should be a single user object
		 * fields I'd like to get:
		 * - name (for display)
		 * - jid (as unique identifier for this user)
		 * - status: one of the possible options, used as a filter
		 * Optional: status message? (not yet displayed anywhere)
		 */
		callback(data);
	    });
	};

	d['send_message'] = function(channel, msg, callback) {
	    $http.post('/message/' + channel, msg).success(function(data) {
		/* msg will be a dict, on django's side this works like
		 * any other form
		 * Jarus: you should choose which fields this call needs
		 */
		callback(data);
	    });
	};
	return d;
    }]);
