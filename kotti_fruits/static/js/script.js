/* Put your content type specific Javascript here. */

$(function() {
    alert('Hello World!');
});

var myApp = angular.module('myApp', []);

myApp.directive('myWidget', function() {
    var linkFn;
    linkFn = function(scope, element, attrs) {
        var animateDown, animateRight, pageOne, pageTwo;
        pageOne = angular.element(element.children()[0]);
        pageTwo = angular.element(element.children()[1]);

        animateDown = function() {
            $(this).animate({
                top: '+=50'
            });
        };

        animateRight = function() {
            $(this).animate({
                left: '+=50'
            });
        };

        $(pageOne).on('click', animateDown);
        $(pageTwo).on('click', animateRight);
    };
    return {
        restrict: 'E',
        link: linkFn
    };
});
