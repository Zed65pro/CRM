from django.urls import path
from .views import JobOrderListCreateView, JobOrderRetrieveUpdateDestroyView,JobOrderImageCreateAPIView

urlpatterns = [
    path('', JobOrderListCreateView.as_view(), name='joborder-list-create'),
    path('<int:pk>/', JobOrderRetrieveUpdateDestroyView.as_view(), name='joborder-detail'),
    path('image/<int:jobId>/', JobOrderImageCreateAPIView.as_view(), name='joborder_image'),
]
