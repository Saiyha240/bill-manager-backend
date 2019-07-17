from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path('orders/', OrderList.as_view(), name="order-list"),
    # path('orders/<int:pk>/', OrderList.as_view(), name="order-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
