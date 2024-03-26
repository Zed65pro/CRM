from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from .models import Customer, Service
from .serializers import (
    CustomerSerializer,
    ServiceSerializer,
    UserSerializer
)

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 6  # Set the desired page size

class CurrentUserView(APIView):
    """
    Retrieve the currently authenticated user.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

class CustomerListCreateView(APIView):
    """
    List all customers or create a new customer.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = Customer.objects.all()
        search_param = request.query_params.get('search', None)
        filter_type = request.query_params.get('filter_type', None)

        if search_param and filter_type:
            field_mapping = {
                'first_name': 'first_name__icontains',
                'last_name': 'last_name__icontains',
                'phone_number': 'phone_number__icontains',
                'address': 'address__icontains',
                'service': 'services__name__icontains',
            }

            field = field_mapping.get(filter_type)
            if field:
                queryset = queryset.filter(Q(**{field: search_param}))

        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetailView(APIView):
    """
    Retrieve, update or delete a customer instance.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk):
        return get_object_or_404(Customer, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ServiceListCreateView(APIView):
    """
    List all services or create a new service.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = Service.objects.all()
        search_param = request.query_params.get('search', None)

        if search_param:
            queryset = queryset.filter(
                Q(name__icontains=search_param)
            )

        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllServicesView(APIView):
    """
    Retrieve all services without pagination.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ServiceDetailView(APIView):
    """
    Retrieve, update or delete a service instance.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk):
        return get_object_or_404(Service, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        service = self.get_object(pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RemoveServiceFromCustomerView(APIView):
    """
    Remove a service from a customer.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, customer_id, service_id, *args, **kwargs):
        customer = get_object_or_404(Customer, id=customer_id)
        service = get_object_or_404(Service, id=service_id)
        
        customer.services.remove(service)
        return Response(status=status.HTTP_200_OK)

class AddServiceToCustomerView(APIView):
    """
    Add a service to a customer.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, customer_id, service_id, *args, **kwargs):
        customer = get_object_or_404(Customer, id=customer_id)
        service = get_object_or_404(Service, id=service_id)
        
        customer.services.add(service)
        return Response(status=status.HTTP_200_OK)
