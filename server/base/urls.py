from django.urls import path
from .views import AllServicesView,CustomerListCreateView,CurrentUserView, ServiceListCreateView,CustomerDetailView,RemoveServiceFromCustomerView,AddServiceToCustomerView,ServiceDetailView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/all/', AllServicesView.as_view(), name='service-get-all'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path(
        'customers/<int:pk>/remove-service/<slug:service_id>',
        RemoveServiceFromCustomerView.as_view(),
        name='remove-service-from-customer'
    ),
    path(
        'customers/<int:pk>/add-service/<slug:service_id>',
        AddServiceToCustomerView.as_view(),
        name='add-service-to-customer'
    ),
    path('user/me/', CurrentUserView.as_view(), name='current_user'),
    # Add more paths for specific views if needed
]
