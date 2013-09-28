angular.module('controllers',[])
  .controller('ChatCtrl', ['$scope', 'RosterGetter', function($scope, RosterGetter){
      $scope.messages = {Jarus: [{user: 'Jarus',
				  message: 'Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test',
				  time: 'Sept 26th, 2013 8:18 PM CET'},
				 {user: 'Gentle',
				  message: 'Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test',
				  time: 'Sept 26th, 2013 8:16 PM CET'}],
			 Gentle: [{user: 'Yarus',
				   message: "blub",
				   time: "Sept 27th, 2013 12:40 AM CET"}]
			};
      $scope.users = [{name: 'Jarus',
		       status: "Online",
		       unread: ""},
		      {name: 'Gentle',
		       status: "Away",
		       unread: "(1)"}
		     ];

      $scope.set_current_user = function(user) {
	  $scope.current_user = user;
	  for (id in $scope.users) {
	      if ($scope.users[id].name == user) {
		  $scope.users[id].unread = "";
		  break;
	      };
	  };
      };

      RosterGetter.get(function(data){
	  $scope.users = data;
      });
      
      $scope.message_order = 'time';
      $scope.user_order = 'name'
      $scope.current_user = 'Jarus';
  }]);
