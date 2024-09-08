from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FormData
from .serializers import FormDataSerializer

class SaveDataView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FormDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Save data to a JSON file
            import json
            from pathlib import Path
            data = serializer.data
            file_path = Path('form_data.json')
            with open(file_path, 'a') as json_file:
                json.dump(data, json_file)
                json_file.write('\n')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.generics import ListAPIView
from .models import FormData
from .serializers import FormDataSerializer
from rest_framework.filters import SearchFilter

class SearchFormDataView(ListAPIView):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
