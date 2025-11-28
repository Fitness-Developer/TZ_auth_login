from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from auth_app.permissions import HasResourcePermission

class ProductsView:
    resource_code = 'products'


@api_view(['GET'])
@permission_classes([HasResourcePermission])
def products(request):
    request.resolver_match.func.view_class = ProductsView
    products = [
        {'id': 1, 'title': 'Product A'},
        {'id': 2, 'title': 'Product B'}
    ]
    return Response(products)

class OrdersView:
    resource_code = 'orders'


@api_view(['GET'])
@permission_classes([HasResourcePermission])
def orders(request):
    request.resolver_match.func.view_class = OrdersView
    return Response([{'id': 1, 'total': 100}, {'id': 2, 'total': 200}])

urlpatterns = [
    path('products/', products),
    path('orders/', orders),
]
