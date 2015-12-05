var app = angular.module('personal-page', ['ngRoute']);

app.config(['$routeProvider','$locationProvider',
function($routeProvider, $locationProvider) {
    $routeProvider.
        when('/',{
            templateUrl: 'main.html'
        }).
        when('/register', {
            templateUrl: 'register.html'
        }).
        when('/order', {
            templateUrl: 'order.html'
        }).
        when('/tracking', {
            templateUrl: 'tracking.html'
        }).
        otherwise({
            redirectTo: '/'
        });
    $locationProvider.html5Mode(true);
}]);

app.controller("PanelController", function() {
 this.tab = 0;
 this.returnTab = function() {
     return this.tab;
 };
 this.selectTab = function(setTab) {
     this.tab = setTab;
 };

 this.isSelected = function(checkTab) {
    return this.tab === checkTab;
 };
});

app.controller("ContactController", function() {
this.lang = 0;
this.selectLang = function(setLang){
    this.lang = setLang;
};
this.isSelected = function(checkLang) {
    return this.lang === checkLang;
};
});

app.controller("FooterController", function() {
 this.twitter = 'twitter.png';
 this.github = 'github.png';
 this.facebook = 'facebook.png';
 this.google = 'google+.png';
 this.linkedin = 'linkedin.png';

 this.activate = function(element) {
    switch (element) {
        case "twitter":
            this.twitter= "twitter-active.png";
            break;
        case "github":
            this.github = "github-active.png";
            break;
        case "facebook":
            this.facebook = "facebook-active.png";
            break;
        case "google":
            this.google = "google+-active.png";
            break;
        case "linkedin":
            this.linkedin = "linkedin-active.png";
            break;
    }
    return;
 };
 this.deactivate = function(element) {
    switch (element) {
        case "twitter":
            this.twitter= "twitter.png";
            break;
        case "github":
            this.github = "github.png";
            break;
        case "facebook":
            this.facebook = "facebook.png";
            break;
        case "google":
            this.google = "google+.png";
            break;
        case "linkedin":
            this.linkedin = "linkedin.png";
            break;
    }
    return;
 }
});

// <html ng-app="store">
// <body ng-controller="StoreController as store">
// <h1 ng-show="name"> Hello, {{name}}! </h1>
// <li ng-repeat="Prodoct in store.products"> {{product.name}} </li>
// {{something | filter}}
