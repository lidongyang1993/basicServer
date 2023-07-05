from django.db import models
from django.db.models import QuerySet


class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeleteQuerySet, self).update(is_use=False)

    def thorough_delete(self):
        return super(SoftDeleteQuerySet, self).delete()


class Manager(models.Manager):
    """支持软删除查询"""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model).filter(is_use=True)

    def get_queryset_in_deleted(self):
        return SoftDeleteQuerySet(self.model).filter()


class PropertyManager(Manager):
    pass
