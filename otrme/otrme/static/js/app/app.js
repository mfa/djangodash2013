angular.module('OtrMe', ['ngCookies', 'controllers', 'services'])
    .config(function ($httpProvider)  {
	$httpProvider.defaults.withCredentials = true;
    });
