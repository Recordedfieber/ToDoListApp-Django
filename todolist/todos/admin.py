from django.contrib import admin

# Registers your models here.
from .models import TodoTask

# Registers your models here.
admin.site.register(TodoTask)