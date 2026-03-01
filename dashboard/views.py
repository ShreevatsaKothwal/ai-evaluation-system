from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Max, Min
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login

from exams.models import Exam, Submission, Question
from .forms import RegisterForm
import json

# ======================================================
# 🔹 ANALYTICS SECTION
# ======================================================

@login_required
def exam_dashboard(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    submissions = Submission.objects.filter(exam=exam)

    total_students = submissions.count()

    if total_students == 0:
        context = {
            "exam": exam,
            "total_students": 0,
            "average_score": 0,
            "highest_score": 0,
            "lowest_score": 0,
            "pass_percentage": 0,
        }
        return render(request, "dashboard/exam_dashboard.html", context)

    average_score = submissions.aggregate(Avg("total_score"))["total_score__avg"]
    highest_score = submissions.aggregate(Max("total_score"))["total_score__max"]
    lowest_score = submissions.aggregate(Min("total_score"))["total_score__min"]

    pass_count = submissions.filter(
        total_score__gte=exam.total_marks * 0.4
    ).count()

    pass_percentage = (pass_count / total_students) * 100
    fail_count = total_students - pass_count

    context = {
        "exam": exam,
        "total_students": total_students,
        "average_score": round(average_score, 2),
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "pass_percentage": round(pass_percentage, 2),
        "pass_count": pass_count,
        "fail_count": fail_count,
    }

    return render(request, "dashboard/exam_dashboard.html", context)


@login_required
def submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    return render(request, "dashboard/submission_detail.html", {
        "submission": submission,
        "answers": submission.answers.all()
    })


# ======================================================
# 🔹 CONFIGURE SECTION (STAFF ONLY)
# ======================================================

@login_required
@staff_member_required
def configure_dashboard(request):
    exams = Exam.objects.all()
    return render(request, "dashboard/configure_dashboard.html", {
        "exams": exams
    })


@login_required
@staff_member_required
def add_exam(request):

    if request.method == "POST":
        name = request.POST.get("name")
        total_marks = request.POST.get("total_marks")

        Exam.objects.create(
            name=name,
            total_marks=total_marks
        )

        return redirect("configure_dashboard")

    return render(request, "dashboard/add_exam.html")


@login_required
@staff_member_required
def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == "POST":
        exam.name = request.POST.get("name")
        exam.total_marks = request.POST.get("total_marks")
        exam.save()
        return redirect("configure_dashboard")

    return render(request, "dashboard/edit_exam.html", {
        "exam": exam
    })


@login_required
@staff_member_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == "POST":
        exam.delete()
        return redirect("configure_dashboard")

    return render(request, "dashboard/delete_exam.html", {
        "exam": exam
    })


# ======================================================
# 🔹 QUESTION MANAGEMENT
# ======================================================

@login_required
@staff_member_required
def manage_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()

    total_marks = sum(q.max_marks for q in questions)

    return render(request, "dashboard/manage_questions.html", {
        "exam": exam,
        "questions": questions,
        "total_marks": total_marks
    })


@login_required
@staff_member_required
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == "POST":
        question_code = request.POST.get("question_code")
        max_marks = request.POST.get("max_marks")
        rubric_str = request.POST.get("rubric")

        try:
            rubric = json.loads(rubric_str)
        except Exception as e:
            print("Invalid rubric JSON:", e)
            rubric = {}

        Question.objects.create(
            exam=exam,
            question_code=question_code,
            max_marks=max_marks,
            rubric=rubric
        )

        # Auto update total marks
        total_marks = sum(q.max_marks for q in exam.questions.all())
        exam.total_marks = total_marks
        exam.save()

        return redirect("manage_questions", exam_id=exam.id)

    return render(request, "dashboard/add_question.html", {
        "exam": exam
    })


# ======================================================
# 🔹 STUDENT DASHBOARD
# ======================================================

@login_required
def student_dashboard(request):
    submissions = request.user.submissions.all()

    return render(request, "dashboard/student_dashboard.html", {
        "submissions": submissions
    })


# ======================================================
# 🔹 REGISTER VIEW
# ======================================================

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)   # auto login
            return redirect("student_dashboard")
    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form
    })




