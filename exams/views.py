from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Exam, Submission, Answer
from evaluation.ocr import extract_text_from_image
from evaluation.scoring import calculate_score
from evaluation.feedback import generate_feedback
from .models import Exam


def home(request):
    exams = Exam.objects.all()
    return render(request, "home.html", {"exams": exams})

@login_required
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # Prevent duplicate submission
    existing_submission = Submission.objects.filter(
        student=request.user,
        exam=exam
    ).first()

    if existing_submission:
        return redirect('submission_detail', submission_id=existing_submission.id)

    if request.method == 'POST':

        with transaction.atomic():

            submission = Submission.objects.create(
                student=request.user,
                exam=exam
            )

            for question in exam.questions.all():

                image = request.FILES.get(f"question_{question.id}")

                if not image:
                    continue

                answer = Answer.objects.create(
                    submission=submission,
                    question=question,
                    uploaded_image=image
                )

                try:
                    # OCR
                    image_path = answer.uploaded_image.path
                    extracted_text = extract_text_from_image(image_path)
                    answer.extracted_text = extracted_text

                    # Hybrid Deterministic Scoring
                    result = calculate_score(answer)

                    answer.marks_awarded = result["total"]
                    answer.breakdown = result["breakdown"]

                    # Groq Feedback (NOT used for scoring)
                    feedback = generate_feedback(answer)
                    answer.feedback = feedback

                    answer.save()

                    print("Generated feedback:", feedback)

                except Exception as e:
                    print("Error during processing:", e)
                    answer.extracted_text = "Error during processing"
                    answer.marks_awarded = 0
                    answer.feedback = "Feedback generation failed."
                    answer.save()

            #  FINAL TOTAL SCORE CALCULATION
            total = sum(ans.marks_awarded or 0 for ans in submission.answers.all())
            submission.total_score = round(total, 2)
            submission.save()

            print("Final Total Score:", submission.total_score)

        messages.success(request, "Exam submitted and evaluated successfully!")
        return redirect('submission_detail', submission_id=submission.id)

    return render(request, 'submit_exam.html', {'exam': exam})

