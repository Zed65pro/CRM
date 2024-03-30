from django.urls import path
from .views import JobOrderListCreateView, JobOrderRetrieveUpdateDestroyView

urlpatterns = [
    path('', JobOrderListCreateView.as_view(), name='joborder-list-create'),
    path('<int:pk>/', JobOrderRetrieveUpdateDestroyView.as_view(), name='joborder-detail'),
]
