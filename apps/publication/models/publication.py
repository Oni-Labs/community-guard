from django.db import models


class PublicationManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related(
            'create_by',
        ).order_by('-create_at')


class Publication(models.Model):
    # managers
    objects = PublicationManager()

    # fields
    # location = models.ForeignKey(
    #     to='core.Location',
    #     on_delete=models.PROTECT,
    #     related_name='publications_location',
    #     null=True
    # )
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    status = models.BooleanField(default=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(
        to='account.User',
        on_delete=models.PROTECT,
        related_name='publications_user',
        null=True
    )
