import json
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from movies_collection.serializers import MovieDataSerializer, MovieSerializer, CollectionSerializer
from .models import Movie, Collection
from rest_framework import status
from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class MoviePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data
        })


class MovieViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer
    pagination_class = MoviePagination


class CollectionViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Collection.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            movies_serializer = MovieSerializer(
                instance.movies.all(), many=True)
            serializer_data = serializer.data
            serializer_data['movies'] = movies_serializer.data
            return Response(serializer_data)
        except Exception as e:
            return Response({"error": e, "message": "Oops! Something went wrong"})

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            movies_data = request.data.get('movies')
            for movie_data in movies_data:
                movie_data_serializer = MovieDataSerializer(data=movie_data)
                if movie_data_serializer.is_valid(raise_exception=True):
                    pass
            if serializer.is_valid():
                collection = serializer.save()
                response_data = {
                    'collection_uuid': collection.uuid
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                error_message = serializer.errors
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except AssertionError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            response_data = []
            for collection in serializer.data:
                collection_obj = Collection.objects.get(
                    uuid=collection['uuid'])
                movies_serializer = MovieSerializer(
                    collection_obj.movies.all(), many=True)
                collection['movies'] = movies_serializer.data
                response_data.append(collection)
            return Response(response_data)
        except Exception as e:
            return Response({"error": e, "message": "Oops! Something went wrong"})

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'Collection deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": e, "message": "Oops! Something went wrong"})

    def perform_destroy(self, instance):
        instance.delete()
