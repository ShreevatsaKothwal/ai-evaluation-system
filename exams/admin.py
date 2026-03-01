from django.contrib import admin
from .models import Exam, Question, Submission, Answer
# Register your models here.



admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Answer)