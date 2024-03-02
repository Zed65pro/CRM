from rest_framework import generics,status
from .models import Customer, Service
from .serializers import CustomerSerializer, ServiceSerializer,UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user
    

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

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