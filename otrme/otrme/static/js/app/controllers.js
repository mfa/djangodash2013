// this helps when debugging, does more or less what python's dir does
function dir(object) {
    stuff = [];
    for (s in object) {
	stuff.push(s);
    }
    stuff.sort();
    return stuff;
};

function pretty_hash(object) {
    result = '{';
    for (key in object) {
	result = result + key + ':"' + object[key] + '", ';
    };
    result = result + '}';
    return result
};

angular.module('controllers',[])
  .controller('ChatCtrl', ['$scope', 'OtrmeApi', function($scope, OtrmeApi){

      $scope.pretty_unread = function(unread) {
	  if (parseInt(unread) > 0) {
	      return "("+unread+")";
	  };
	  return "";
      };

      $scope.pretty_otr = function(status) {
	  result = ""
	  if (status) {
	      result = '<i class="glyphicon glyphicon-lock"></i> OTR enabled | '
	  };
	  return result;
      };

      /************************************************************************
       * Messaging related
       */
      $scope.send_message = function(channel, msgtext) {
	  var message = {};
	  var d = new Date();
	  message['time'] = d.toString();
	  message['message'] = msgtext;
	  message['jid'] = $scope.own_jid;
	  OtrmeApi.send_message(channel, message, function(data) {
	      $scope.add_message(channel, message);
	  });
      };

      $scope.add_message = function(channel, msg) {
	  if (!$scope.messages[channel]) {
	      $scope.messages[channel] = [];
	  };
	  $scope.messages[channel].push(msg)
	  // notification of any kind here?
	  if (channel != $scope.current_channel_name) {
	      var user = $scope.get_user(channel);
	      if (!user.unread) {
		  user.unread = 0
	      };
	      user.unread = user.unread + 1;
	  };
      };

      /***********************************************************************/

      $scope.get_user = function(jid) {
	  for (id in $scope.users) {
	      if ($scope.users[id].jid == jid) {
		  return $scope.users[id];
	      };
	  };
	  return null;
      };

      $scope.current_user = function() {
	  return $scope.get_user($scope.current_channel_name);
      };

      $scope.set_current_channel = function(channel) {
	  var old_channel = $scope.current_channel_name;
	  $scope.cached_input[old_channel] = $scope.new_message_text;
	  if ($scope.cached_input[channel]) {
	      $scope.new_message_text = $scope.cached_input[channel];
	  } else {
	      $scope.new_message_text = "";
	  };
	  OtrmeApi.set_focus(channel);
	  $scope.current_channel_name = channel;
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
	      obj = JSON.parse(msg.data);
	      if (obj.message !== null) {
		  $scope.add_message(obj.jid, obj);
	      };
	  });
      };
      es.addEventListener('message', handleMessage, false);

      var handleRoster = function() {
	  $scope.$apply(function () {
	      OtrmeApi.get_roster(function(data){
		  $scope.users = data;
		  if (!$scope.current_channel_name) {
		      $scope.set_current_channel($scope.users[1].jid);
		  };
	      });
	  });
      };
      es.addEventListener('roster_updated', handleRoster, false);

      var handleStatus = function(data) {
	  $scope.apply(function () {
	      obj = JSON.parse(data.data);
	      if (!$scope.get_user(data.jid)) {
		  $scope.users.push(data);
	      } else {
		  var user = $scope.get_user(data.jid);
		  user.show = data.show;
		  user.status = data.status;
	      };
	  });
      };
      es.addEventListener('status_changed', handleStatus, false);

      /************************************************************************
       * Init and default values
       */
      OtrmeApi.get_roster(function(data){
	  $scope.users = data;
	  $scope.set_current_channel($scope.users[1].jid);
      });

      $scope.messages = {};
      $scope.users = [];
      $scope.current_channel_name = '';
      $scope.new_message_text = '';
      $scope.own_jid = logged_in_jid;
      $scope.cached_input = {};
  }]);
