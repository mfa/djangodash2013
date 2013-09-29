angular.module('controllers',[])
  .controller('ChatCtrl', ['$scope', 'OtrmeApi', function($scope, OtrmeApi){
      /************************************************************************
       * mockup data
       */
      $scope.messages = {Jarus: [{user: 'Jarus',
				  jid: 'otr@jabme.de',
				  message: 'Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test',
				  time: 'Sept 26th, 2013 8:18 PM CET'},
				 {user: 'Gentle',
				  message: 'Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test',
				  time: 'Sept 26th, 2013 8:16 PM CET'}],
			 Gentle: [{user: 'Jarus',
				   message: "blub",
				   time: "Sept 27th, 2013 12:40 AM CET"}]
			};
      $scope.users = [{name: 'Jarus',
		       jid: 'otr@jabme.de',
		       status: "Online",
		       unread: 0},
		      {name: 'Gentle',
		       jid: 'dastier@schokokeks.org',
		       status: "Away",
		       unread: 1}
		     ];

      /***********************************************************************/

      OtrmeApi.get_roster(function(data){
	  $scope.users = data;
      });

      $scope.pretty_unread = function(unread) {
	  if (parseInt(unread) > 0) {
	      return "("+unread+")";
	  };
	  return "";
      };

      /************************************************************************
       * Messaging related
       */
      $scope.send_message = function(channel, msgtext) {
	  var message = {};
	  var d = new Date();
	  message['time'] = d.toString();
	  message['message'] = msgtext;
	  message['user'] = 'Gentle';
	  $scope.add_message(channel, message);
      };

      $scope.add_message = function(channel, msg) {
	  if (!$scope.messages[channel]) {
	      $scope.messages[channel] = [];
	  };
	  $scope.messages[channel].push(msg)
      };

      /***********************************************************************/

      $scope.current_user = function() {
	  for (id in $scope.users) {
	      if ($scope.users[id].name == $scope.current_user_name) {
		  return $scope.users[id];
	      };
	  };
	  return null;
      };
      $scope.set_current_user = function(user) {
	  var old_user = $scope.current_user_name;
	  $scope.cached_input[old_user] = $scope.new_message_text;
	  if ($scope.cached_input[user]) {
	      $scope.new_message_text = $scope.cached_input[user];
	  } else {
	      $scope.new_message_text = "";
	  };
	  $scope.current_user_name = user;
	  $scope.current_user().unread = 0;
      };

      /************************************************************************
       * SSE Event Handlers
       */
      var es = new EventSource('/events/');

      var handleMessage = function(msg) {
	  // apply is needed since this function gets called asynchronously
	  // but needs to update angular's scope (thread) context
	  $scope.$apply(function () {
	      // I  have no messages to test with yet :P
	  });
      };
      es.addEventListener('message', handleMessage, false);

      /************************************************************************
       * Init and default values
       */
      $scope.current_user_name = 'Jarus';
      $scope.new_message_text = '';
      $scope.cached_input = {};
  }]);
