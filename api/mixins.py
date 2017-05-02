from django.db import models
from django.contrib.auth.models import User


class ReviewMixin(models.Model):

    class Meta:
        abstract = True

    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s")
    post_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
