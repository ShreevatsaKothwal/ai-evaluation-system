from django.urls import path
from . import views

urlpatterns = [

    # 👨‍🎓 Student Dashboard (default dashboard/)
    path("", views.student_dashboard, name="student_dashboard"),

    path(
        "configure/exam/<int:exam_id>/questions/",
        views.manage_questions,
        name="manage_questions"
    ),
    # Question Management
    path(
        "configure/exam/<int:exam_id>/questions/add/",
        views.add_question,
        name="add_question"
    ),

    # 🔵 QUESTION MANAGEMENT (Phase 2)
    path(
        "configure/exam/<int:exam_id>/questions/",
        views.manage_questions,
        name="manage_questions"
    ),
    path("register/", views.register_view, name="register"),

    # 🔵 Configure Exams
    path("configure/exam/add/", views.add_exam, name="add_exam"),
    path("configure/exam/<int:exam_id>/edit/", views.edit_exam, name="edit_exam"),
    path("configure/exam/<int:exam_id>/delete/", views.delete_exam, name="delete_exam"),
    path("configure/", views.configure_dashboard, name="configure_dashboard"),

    # 🔵 Analytics
    path("exam/<int:exam_id>/", views.exam_dashboard, name="exam_dashboard"),
    path("submission/<int:submission_id>/", views.submission_detail, name="submission_detail"),
]