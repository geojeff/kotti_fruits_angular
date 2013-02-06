/* Put your content type specific Javascript here. */

var myApp = angular.module('myApp', []);

console.log('hey 0');
myApp.directive('myWidget', function() {
    var linkFn;
    console.log('hey 1');
    linkFn = function(scope, element, attrs) {
        var animateDown, animateRight, pageOne, pageTwo;
        console.log('hey 2');
        pageOne = angular.element(element.children()[0]);
        pageTwo = angular.element(element.children()[1]);

        animateDown = function() {
            console.log('hey 3');
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
