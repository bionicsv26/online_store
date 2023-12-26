from django.db import models
from django.db.models import options


options.DEFAULT_NAMES += ('permissions_model', )

# Для корректной работы сигнала каждая модель должна иметь в классе Meta
# поле permissions_model по аналогии с образцом ниже
# class BaseModel(models.Model):
#     class Meta:
#
#         permissions_model = {
#             "Customer": (f"add_basemodel",
#                          f"view_basemodel"),
#             "Moderator": (f"add_basemodel",
#                           f"change_basemodel",
#                           f"view_basemodel"),
#             "Administrator": (f"add_basemodel",
#                               f"change_basemodel",
#                               f"delete_basemodel",
#                               f"view_basemodel")
#         }
