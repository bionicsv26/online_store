from django.db import models
from django.db.models import options


options.DEFAULT_NAMES += ('permissions_model', )


# class BaseModel(models.Model):
#
#     permissions_model = {
#         "Customer": (f"add_basemodel",
#                      f"view_basemodel"),
#         "Moderator": (f"add_basemodel",
#                       f"change_basemodel",
#                       f"view_basemodel"),
#         "Administrator": (f"add_basemodel",
#                           f"change_basemodel",
#                           f"delete_basemodel",
#                           f"view_basemodel")
#     }
