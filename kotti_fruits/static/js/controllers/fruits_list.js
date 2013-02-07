function FruitsListCtrl($scope, $http) {
  $http.get('/fruits').success(function(data) {
    $scope.fruits = data;
  });
 
  $scope.orderProp = 'calories';
}
 
//FruitsListCtrl.$inject = ['$scope', '$http'];
