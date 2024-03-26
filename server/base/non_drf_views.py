from django.http import JsonResponse #to return Json response to frontend
from django.views import View
from django.shortcuts import get_object_or_404 # extra functionality to get_object and raise 404 error if not found
from django.db.models import Q # for better Query support
import json # to load post, updata bodies from frontend 
from .models import Customer, Service #models
from .serializers import CustomerSerializer, ServiceSerializer, UserSerializer  #serializers
from django.views.decorators.csrf import csrf_exempt # to remove crsf(cross site request forgery protection) which is disadvantage but we have to do here
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Custom pagination class
class CustomPageNumberPagination:
    page_size = 6

# Retrieve current user view
class CurrentUserView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            print(request.user)
            return JsonResponse({'error': 'User not authenticated'}, status=403)
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data)

# Customer List and Create View
class CustomerListCreateView(View):
    def get(self, request, *args, **kwargs):
        queryset = Customer.objects.all()
        search_param = request.GET.get('search', None)
        filter_type = request.GET.get('filter_type', None)

        if search_param and filter_type:
            field_mapping = {
                'first_name': 'first_name__icontains',
                'last_name': 'last_name__icontains',
                'phone_number': 'phone_number__icontains',
                'address': 'address__icontains',
                'service': 'services__name__icontains',
            }

            field = field_mapping.get(filter_type,None)
            if field:
                queryset = queryset.filter(Q(**{field: search_param}))
        
        # Implementing Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, CustomPageNumberPagination.page_size)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        serializer = CustomerSerializer(queryset,many=True)
        return JsonResponse(serializer.data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.body)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Customer Detail View
class CustomerDetailView(View):
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('pk',None)
        if not customer_id:
            return JsonResponse({'error': 'Customer id is required.'}, status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        serializer = CustomerSerializer(customer)
        return JsonResponse(serializer.data)

    @csrf_exempt
    def patch(self, request, *args, **kwargs):
        customer_id = kwargs.get('pk',None)
        if not customer_id:
            return JsonResponse({'error': 'Customer id is required.'}, status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        serializer = CustomerSerializer(customer, data=request.body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        customer_id = kwargs.get('pk',None)
        if not customer_id:
            return JsonResponse({'error': 'Customer id is required.'}, status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return JsonResponse({'message': 'Customer deleted successfully.'})

# Service List and Create View
class ServiceListCreateView(View):
    def get(self, request, *args, **kwargs):
        queryset = Service.objects.all()
        search_param = request.GET.get('search', None)

        if search_param:
            queryset = queryset.filter(Q(name__icontains=search_param))

        # Implementing Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, CustomPageNumberPagination.page_size)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        serializer = ServiceSerializer(queryset,many=True)
        return JsonResponse(serializer.data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Admin access required.'}, status=403)
        serializer = ServiceSerializer(data=request.body)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Get all services without pagination
class AllServicesView(View):
    @login_require
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        serializer = ServiceSerializer(services,many=True)
        return JsonResponse(serializer.data)

# Service Detail View
class ServiceDetailView(View):
    def get(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        if not service_id:
            return JsonResponse({'error': 'Service id is required.'}, status=400)
        service = get_object_or_404(Service, id=service_id)
        serializer = ServiceSerializer(service)
        return JsonResponse(serializer.data)

    @csrf_exempt
    def patch(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        service = get_object_or_404(Service, id=service_id)
        serializer = ServiceSerializer(service, data=request.body)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        service = get_object_or_404(Service, id=service_id)
        service.delete()
        return JsonResponse({'message': 'Service deleted successfully.'})

# Remove Service From Customer View
class RemoveServiceFromCustomerView(View):
    @csrf_exempt
    def patch(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        service_id = kwargs.get('service_id')
        if not customer_id or not service_id:
            return JsonResponse({'message': 'Missing customer_id or service_id.'}, status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        service = get_object_or_404(Service, id=service_id)
        customer.services.remove(service)
        return JsonResponse({'message': 'Service removed from customer successfully.'})

# Add Service To Customer View
class AddServiceToCustomerView(View):
    @csrf_exempt
    def patch(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        service_id = kwargs.get('service_id')
        if not customer_id or not service_id:
            return JsonResponse({'message': 'Missing customer_id or service_id.'}, status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        service = get_object_or_404(Service, id=service_id)
        customer.services.add(service)
        return JsonResponse({'message': 'Service added to customer successfully.'})
