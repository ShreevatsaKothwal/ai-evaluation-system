from django.db import models
from django.conf import settings
from exams.models import Exam, Question
# Create your models here.
from django.db import models

breakdown = models.JSONField(null=True, blank=True)