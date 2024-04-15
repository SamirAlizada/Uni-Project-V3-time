from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # ***  Panel  ***

    # General
    path('panel-lessons/', login_required(panel_lessons), name='panel_lessons'),
    path('teacher-panel/', login_required(teacher_panel), name='teacher_panel'),
    path('classroom-panel/', login_required(classroom_panel), name='classroom_panel'),
    path('group-panel/', login_required(group_panel), name='group_panel'),

    # Lesson
    path('add-lesson/', login_required(add_lesson), name='add_lesson'),
    path('delete-lesson/<int:pk>/', login_required(delete_lesson), name="delete_lesson"),
    path("update-lesson/<int:pk>/", login_required(update_lesson), name="update_lesson"),

    # Classroom
    path('add-classroom/', login_required(add_classroom), name='add_classroom'),
    path('delete-classroom/<int:pk>/', login_required(delete_classroom), name="delete_classroom"),
    path("update-classroom/<int:pk>/", login_required(update_classroom), name="update_classroom"),

    # Teacher
    path('add-teacher/', login_required(add_teacher), name='add_teacher'),
    path('delete-teacher/<int:pk>/', login_required(delete_teacher), name="delete_teacher"),
    path("update-teacher/<int:pk>/", login_required(update_teacher), name="update_teacher"),
    
    # Group
    path('add-group/', login_required(add_group), name='add_group'),
    path('delete-group/<int:pk>/', login_required(delete_group), name="delete_group"),
    path("update-group/<int:pk>/", login_required(update_group), name="update_group"),

    # -----------------------------------------------------------------------

    # All lessons
    path('table-only-lessons/', login_required(table_lessons_filtered_list), name='table_only_lessons'),

    # Weekly lessons
    path('weekly-only-lessons/', weekly_limited_filtered_lessons, name='weekly_only_lessons'),
    
    # Daily lessons
    path('', daily_limited_filtered_lessons, name='daily_only_lessons'),   

    # Account
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    
    path('about/', about, name='about'),

    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('daily_only_lesson_to_pdf/', daily_only_lesson_to_pdf, name='daily_only_lesson_to_pdf')

    
]
