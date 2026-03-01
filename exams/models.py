from django.db import models
from django.conf import settings


class Exam(models.Model):
    name = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_code = models.CharField(max_length=10)  # 1A, 1B, 2A...
    max_marks = models.IntegerField()

    # 🔥 Structured Rubric Storage
    rubric = models.JSONField()

    def __str__(self):
        return f"{self.exam.name} - {self.question_code}"


class Submission(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    # 🔥 Total Score (auto calculated)
    total_score = models.FloatField(default=0)

    class Meta:
        unique_together = ('student', 'exam')

    def __str__(self):
        return f"{self.student} - {self.exam.name}"


class Answer(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    uploaded_image = models.ImageField(upload_to='answer_images/')
    extracted_text = models.TextField(blank=True)
    marks_awarded = models.FloatField(null=True, blank=True)

    # 🔥 NEW: Section-wise rubric breakdown
    breakdown = models.JSONField(null=True, blank=True)

    # 🔥 Store Groq feedback (already JSON)
    feedback = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.submission.student} - {self.question.question_code}"