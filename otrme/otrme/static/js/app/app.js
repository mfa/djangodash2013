angular.module('OtrMe', ['controllers', 'services'])
    .config(function ($httpProvider)  {
	$httpProvider.defaults.withCredentials = true;
    });
