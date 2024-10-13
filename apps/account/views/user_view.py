from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


from apps.account.serializers import CreateUserSerializer
from apps.account.models import User


class CreateUserAPIView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=HTTP_201_CREATED)

        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListUserAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        users = User.objects.values(
            'username', 'email', 'is_active', 'is_superuser'
        )

        return Response(data=users, status=HTTP_200_OK)



