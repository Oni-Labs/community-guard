from django.urls import path

from apps.account.views import CreateUserAPIView, ListUserAPIView

urlpatterns = [
    path('users/', ListUserAPIView.as_view(), name='list_users_api'),
    path('user/create/', CreateUserAPIView.as_view(), name='create_user_api')
]