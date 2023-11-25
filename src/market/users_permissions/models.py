from django.db import models
from django.db.models import options


options.DEFAULT_NAMES += ('permissions_model', )


class Post(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        permissions_model = {"Customer": ("add_post", "view_post"),
                             "Moderator": ("add_post", "change_post", "view_post"),
                             "Administrator": ("add_post", "change_post", "delete_post", "view_post")}
