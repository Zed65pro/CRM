from rest_framework import generics,status
from .models import Customer, Service
from django.db.models import Q
from .serializers import CustomerSerializer, ServiceSerializer,UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 6  # Set the desired page size

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def get_queryset(self):
        queryset = super().get_queryset()
        search_param = self.request.query_params.get('search', None)
        filter_type = self.request.query_params.get('filter_type', None)

        if search_param and filter_type:
            # Use a dictionary to map filter_type to corresponding fields
            field_mapping = {
                'first_name': 'first_name__icontains',
                'last_name': 'last_name__icontains',
                'phone_number': 'phone_number__icontains',
                'address': 'address__icontains',
                'service': 'services__name__icontains',  # Add this line for services.name
            }

            # Dynamically construct the Q object based on filter_type
            field = field_mapping.get(filter_type)
            if field:
                queryset = queryset.filter(Q(**{field: search_param}))

        return queryset

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = Service.objects.all()
        search_param = self.request.query_params.get('search', None)
        print(search_param)
        if search_param:
            # Use Q objects to perform case-insensitive search on name and description
            queryset = queryset.filter(
                Q(name__icontains=search_param)
            )

        return queryset

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

        
class RemoveServiceFromCustomerView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = ServiceSerializer

    def update(self, request, *args, **kwargs):
        service_id = kwargs.get('service_id', None)
        customer = self.get_object()

        if service_id:
                service = get_object_or_404(Service, id=service_id)
                customer.services.remove(service)
                return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Service ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)

class AddServiceToCustomerView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def update(self, request, *args, **kwargs):
        service_id = kwargs.get('service_id', None)
        customer = self.get_object()

        if service_id:
            service = get_object_or_404(Service, id=service_id)
            customer.services.add(service)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Service ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)