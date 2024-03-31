from rest_framework.response import Response
from rest_framework import generics,status
from .models import JobOrder,JobOrderImage
from .serializers import JobOrderImageSerializer, JobOrderSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 6  # Set the desired page size

class JobOrderListCreateView(generics.ListCreateAPIView):
    queryset = JobOrder.objects.all()
    serializer_class = JobOrderSerializer
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]
        
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        queryset = JobOrder.objects.all()
        search_param = self.request.query_params.get('search', None)

        print(search_param)
        if search_param:
            # Use Q objects to perform case-insensitive search on name and description
            queryset = queryset.filter(
                Q(name__icontains=search_param)
            )
        print(queryset)
        queryset = queryset.prefetch_related('images')
        return queryset

class JobOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobOrder.objects.all()
    serializer_class = JobOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]

class JobOrderImageCreateAPIView(generics.ListCreateAPIView):
    queryset = JobOrderImage.objects.all()
    serializer_class = JobOrderImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self,serializer):
        job_order_id = self.kwargs.get('jobId')
        job_order = get_object_or_404(JobOrder, pk=job_order_id)
        serializer.save(job_order=job_order, uploaded_by=self.request.user)