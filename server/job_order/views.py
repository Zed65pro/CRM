from rest_framework.response import Response
from rest_framework import generics,status
from .models import JobOrder
from .serializers import JobOrderImageSerializer, JobOrderSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination


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

class JobOrderImageCreateAPIView(generics.CreateAPIView):
    serializer_class = JobOrderImageSerializer

    def post(self, request, *args, **kwargs):
        # Ensure job order exists
        job_order_id = request.data.get('job_order')
        try:
            job_order = JobOrder.objects.get(id=job_order_id)
        except JobOrder.DoesNotExist:
            return Response({'error': 'Job order does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Save file
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uploaded_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)