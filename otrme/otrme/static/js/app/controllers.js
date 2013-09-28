angular.module('controllers',[])
  .controller('ChatCtrl', ['$scope', 'RosterGetter', function($scope, RosterGetter){
      /************************************************************************
       * mockup data
       */
      $scope.messages = {Jarus: [{user: 'Jarus',
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
		       status: "Online",
		       unread: 0},
		      {name: 'Gentle',
		       status: "Away",
		       unread: 1}
		     ];
      /***********************************************************************/

      RosterGetter.get(function(data){
	  $scope.users = data;
      });
      
      $scope.pretty_unread = function(unread) {
	  if (parseInt(unread) > 0) {
	      return "("+unread+")";
	  };
	  return "";
      };
      $scope.current_user = function() {
	  for (id in $scope.users) {
	      if ($scope.users[id].name == $scope.current_user_name) {
		  return $scope.users[id];
	      };
	  };
	  return null;
      };
      $scope.set_current_user = function(user) {
	  $scope.current_user_name = user;
	  $scope.current_user().unread = "";
      };
      $scope.current_user_name = 'Jarus';
  }]);
