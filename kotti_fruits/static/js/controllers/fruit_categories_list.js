function FruitCategoriesListCtrl($scope, $http) {
  $http.get('/fruit_categories').success(function(data) {
    $scope.fruit_categories = data;
  });
 
  $scope.orderProp = 'title';
}
 
//FruitCategoriesListCtrl.$inject = ['$scope', '$http'];
