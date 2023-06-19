from rest_framework import serializers
from movies_collection.models import Movie, Collection


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "title",
            "description",
            "genres",
            "uuid",
        ]


class MovieDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "title",
            "description",
            "genres",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    movies = serializers.ListField(write_only=True)

    class Meta:
        model = Collection
        fields = [
            "uuid",
            "title",
            "description",
            "movies",
        ]

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data)
        for movie in movies_data:
            movie = Movie.objects.create(title=movie.get("title"), description=movie.get(
                "description"), genres=movie.get("genres"))
            collection.movies.add(movie)
        return collection
