from django.http import JsonResponse #to return Json response to frontend
from django.views import View
from django.shortcuts import get_object_or_404 # extra functionality to get_object and raise 404 error if not found
from django.db.models import Q # for better Query support
import json # to load post, updata bodies from frontend 

from .models import Customer, Service #models
from .serializers import CustomerSerializer, ServiceSerializer, UserSerializer  #serializers
from django.contrib.auth.decorators import login_required # decorator to check authentication
from django.views.decorators.csrf import csrf_exempt # to remove crsf(cross site request forgery protection) which is disadvantage but we have to do here
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Custom pagination class
class CustomPageNumberPagination:
    page_size = 6

# Retrieve current user view
class CurrentUserView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data)

# Customer List and Create View
class CustomerListCreateView(View):
    @login_required
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
            customers = paginator.page(page)
        except PageNotAnInteger:
            customers = paginator.page(1)
        except EmptyPage:
            customers = paginator.page(paginator.num_pages)

        serializer = CustomerSerializer(queryset,many=True)
        return JsonResponse(serializer.data)

    @login_required
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        customer = json.loads(request.body)
        serializer = CustomerSerializer(data=customer)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Customer Detail View
class CustomerDetailView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('pk',None)
        if not customer_id:
            return JsonResponse({'error': 'Customer id is required.'}, status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        serializer = CustomerSerializer(customer)
        return JsonResponse(serializer.data)

    @login_required
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        customer_id = kwargs.get('pk',None)
        if not customer_id:
            return JsonResponse({'error': 'Customer id is required.'}, status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        data = json.loads(request.body)
        serializer = CustomerSerializer(customer, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    @login_required
    def delete(self, request, *args, **kwargs):
        customer_id = kwargs.get('pk',None)
        if not customer_id:
            return JsonResponse({'error': 'Customer id is required.'}, status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return JsonResponse({'message': 'Customer deleted successfully.'})

# Service List and Create View
class ServiceListCreateView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        queryset = Service.objects.all()
        search_param = request.GET.get('search', None)

        if search_param:
            queryset = queryset.filter(Q(name__icontains=search_param))

        # Implementing Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, CustomPageNumberPagination.page_size)
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)

        serializer = ServiceSerializer(queryset,many=True)
        return JsonResponse(serializer.data)

    @login_required
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Admin access required.'}, status=403)
        data = json.loads(request.body)
        serializer = ServiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Get all services without pagination
class AllServicesView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        serializer = ServiceSerializer(services,many=True)
        return JsonResponse(serializer.data)

# Service Detail View
class ServiceDetailView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        if not service_id:
            return JsonResponse({'error': 'Service id is required.'}, status=400)
        service = get_object_or_404(Service, id=service_id)
        serializer = ServiceSerializer(service)
        return JsonResponse(serializer.data)

    @login_required
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        service = get_object_or_404(Service, id=service_id)
        data = json.loads(request.body)
        serializer = ServiceSerializer(service, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    @login_required
    def delete(self, request, *args, **kwargs):
        service_id = kwargs.get('pk')
        service = get_object_or_404(Service, id=service_id)
        service.delete()
        return JsonResponse({'message': 'Service deleted successfully.'})

# Remove Service From Customer View
class RemoveServiceFromCustomerView(View):
    @login_required
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
    @login_required
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
