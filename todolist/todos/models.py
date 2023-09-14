from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CharField

# from .validators import PriorityValidator
from django.contrib.auth.models import User


class TodoTask(models.Model):

    class meta:
        ordering = ["-task_priority"]

    user = (models.ForeignKey(
                User,
                on_delete=models.CASCADE,
                null=True,
                blank=True
            ))

    task_title = models.CharField(max_length=35)
    task_priority = models.IntegerField(
        # validators=[PriorityValidator()]
        validators=[MinValueValidator(1)]
    )
    task_due_date = models.DateField()
    task_status = models.BooleanField(default=False)

    def __str__(self) -> CharField:
        return self.task_title
