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
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, PolymorphicProxySerializer, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

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

    @extend_schema(responses={
        200: PolymorphicProxySerializer(
                component_name='Person',
                serializers=[CollectionSerializer, MovieSerializer],
                resource_type_field_name='type',
        ),
        400: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "error": {"type": "string", "example": "Invalid input data."}
                    }
                },
                description="Bad Request with error message."
            ),
        403: OpenApiResponse(
                response=OpenApiTypes.STR,
                description="Forbidden",
                examples=[
                    OpenApiExample(
                        'Forbidden Response',
                        value="You do not have permission to perform this action."
                    )
                ]
            ),
    })
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

    @extend_schema(
        # Extra parameters added to the schema
        parameters=[
            OpenApiParameter(name='artist', description='Filter by artist', required=False, type=str),
            OpenApiParameter(
                name='release',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filter by release date',
                examples=[
                    OpenApiExample(
                        'Example 1',
                        summary='Search by Date',
                        description='Valid date example',
                        value='1993-08-23'
                    ),
                    OpenApiExample(
                        'Example 2',
                        summary='Search by Name',
                        description='Name',
                        value='john doe'
                    ),
                ],
            ),
        ],
        # Override default docstring extraction
        description='More descriptive text',
        # Provide Authentication class that deviates from the views default
        auth=None,
        # Change the auto-generated operation name
        operation_id=None,
        # Or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
        # Attach request/response examples to the operation.
        examples=[
            OpenApiExample(
                'Example 1',
                summary='200',
                description='An example of a serialized Song object',
                value={
                    "artist": "Nirvana",
                    "release": "1991-09-24",
                    "title": "Smells Like Teen Spirit",
                    "album": "Nevermind"
                }
            ),
            OpenApiExample(
                'Example 2',
                summary='400',
                description='Another example of a serialized Song object',
                value="There is an errror"
            ),
        ],
    )
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
