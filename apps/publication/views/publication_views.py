from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.publication.serializers import CreatePublicationSerializer, ListPublicationSerializer
from apps.publication.models import Publication


class CreatePublicationAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs) -> Response:
        serializer = CreatePublicationSerializer(
            data=request.data, logged_user=request.user)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListPublicationAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs) -> Response:
        publications = Publication.objects.filter(
            status=True
        )

        serializer = ListPublicationSerializer(instance=publications, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)



