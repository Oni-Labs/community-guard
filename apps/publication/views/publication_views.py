from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK)

from apps.publication.serializers import CreatePublicationSerializer
from apps.publication.models import Publication


class CreatePublicationAPIView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        serializer = CreatePublicationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListPublicationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        publications = Publication.objects.values(
            'title', 'description', 'status', 'create_at', 'create_by',
        )

        return Response(data=publications, status=HTTP_200_OK)



