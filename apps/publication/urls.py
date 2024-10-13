from django.urls import path

from apps.publication.views import (
    CreatePublicationAPIView, ListPublicationAPIView)

urlpatterns = [
    path('create/', CreatePublicationAPIView.as_view(), name='create_publication_api'),
    path('list/', ListPublicationAPIView.as_view(), name='list_publications_api'),
]