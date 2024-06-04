from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson, Teacher, Classroom, Group
from django.contrib import messages
from .forms import LessonForm, LessonFilterForm, ClassroomForm, TeacherForm, GroupForm
from datetime import datetime, timedelta
from django.db.models import F, Q
from django.contrib.auth import authenticate, login, logout

def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            # Get information from the form
            lesson_date = form.cleaned_data['date']
            end_date = form.cleaned_data.get('end_date')
            classroom = form.cleaned_data['classroom']
            time_interval = form.cleaned_data['time_interval']
            teacher = form.cleaned_data['teacher']
            group_numbers = form.cleaned_data['group_number']
            lesson_week = form.cleaned_data.get('lesson_week')
            topic_name = form.cleaned_data['topic_name']
            lesson_type = form.cleaned_data['lesson_type']
            lesson_kind = form.cleaned_data['lesson_kind']

            if lesson_week == 'Normal' and end_date:
                # Set the start date to current_date
                current_date = lesson_date
                start_weekday = lesson_date.weekday()  # Day of the week of start date

                while current_date <= end_date:
                    if current_date.weekday() == start_weekday:
                        # Check for course conflicts
                        existing_lessons = Lesson.objects.filter(date=current_date)

                        existing_classroom_lessons = existing_lessons.filter(classroom=classroom)
                        existing_teacher_lessons = existing_lessons.filter(teacher=teacher)
                        existing_group_lessons = existing_lessons.filter(group_number__in=group_numbers)

                        if existing_classroom_lessons.filter(time_interval=time_interval).exists():
                            messages.error(request, f"{lesson_date} tarixində {time_interval} arasında {classroom.class_number} nömrəli auditoriyada dərs var!")
                            break
                        
                        if existing_teacher_lessons.filter(time_interval=time_interval).exists():
                            messages.error(request, f"{lesson_date} tarixində {time_interval} arasında müəllim {teacher} dərsi var!")
                            break
                        
                        if existing_group_lessons.filter(time_interval=time_interval).exists():
                            messages.error(request, f"{lesson_date} tarixində {time_interval} arasında seçilmiş qrupun artıq dərsi var!")
                            break
                        
                        # If there is no course conflict, add a course
                        lesson_instance = Lesson(
                            classroom=classroom,
                            teacher=teacher,
                            date=current_date,
                            end_date=end_date,
                            topic_name=topic_name,
                            lesson_week=lesson_week,
                            lesson_type=lesson_type,
                            lesson_kind=lesson_kind,
                            time_interval=time_interval
                        )
                        lesson_instance.save()
                        lesson_instance.group_number.set(group_numbers)
                        messages.success(request, f"{current_date} tarixinə dərs uğurla əlavə edildi.")
                    
                    current_date += timedelta(days=1)  # Scroll daily and add lessons only for the same day of the week

                return redirect('add_lesson')

            elif lesson_week in ['Alt', 'Üst'] and end_date:
                current_date = lesson_date
                start_weekday = lesson_date.weekday()

                while current_date <= end_date:
                    if current_date.weekday() == start_weekday:
                        # Check for course conflicts
                        existing_lessons = Lesson.objects.filter(date=current_date)

                        existing_classroom_lessons = existing_lessons.filter(classroom=classroom)
                        existing_teacher_lessons = existing_lessons.filter(teacher=teacher)
                        existing_group_lessons = existing_lessons.filter(group_number__in=group_numbers)

                        if existing_classroom_lessons.filter(time_interval=time_interval).exists():
                            messages.error(request, f"{lesson_date} tarixində {time_interval} arasında {classroom.class_number} nömrəli auditoriyada dərs var!")
                            break
                        
                        if existing_teacher_lessons.filter(time_interval=time_interval).exists():
                            messages.error(request, f"{lesson_date} tarixində {time_interval} arasında müəllim {teacher} dərsi var!")
                            break
                        
                        if existing_group_lessons.filter(time_interval=time_interval).exists():
                            messages.error(request, f"{lesson_date} tarixində {time_interval} arasında seçilmiş qrupun artıq dərsi var!")
                            break
                        
                        # If there is no course conflict, add a course
                        lesson_instance = Lesson(
                            classroom=classroom,
                            teacher=teacher,
                            date=current_date,
                            end_date=end_date,
                            topic_name=topic_name,
                            lesson_week=lesson_week,
                            lesson_type=lesson_type,
                            lesson_kind=lesson_kind,
                            time_interval=time_interval
                        )
                        lesson_instance.save()
                        lesson_instance.group_number.set(group_numbers)
                        messages.success(request, f"{current_date} tarixinə dərs uğurla əlavə edildi.")
                    
                    current_date += timedelta(weeks=2)  # Move forward 2 weeks, i.e. leave 1 week blank
                
                return redirect('add_lesson')

            else:
                # Adding a single course
                existing_lessons = Lesson.objects.filter(date=lesson_date)

                existing_classroom_lessons = existing_lessons.filter(classroom=classroom)
                existing_teacher_lessons = existing_lessons.filter(teacher=teacher)
                existing_group_lessons = existing_lessons.filter(group_number__in=group_numbers)

                if existing_classroom_lessons.filter(time_interval=time_interval).exists():
                    messages.error(request, f"{lesson_date} tarixində {time_interval} arasında {classroom.class_number} nömrəli auditoriyada dərs var!")
                
                elif existing_teacher_lessons.filter(time_interval=time_interval).exists():
                    messages.error(request, f"{lesson_date} tarixində {time_interval} arasında müəllim {teacher} dərsi var!")
                
                elif existing_group_lessons.filter(time_interval=time_interval).exists():
                    messages.error(request, f"{lesson_date} tarixində {time_interval} arasında seçilmiş qrupun artıq dərsi var!")
                
                else:
                    lesson_instance = Lesson(
                        classroom=classroom,
                        teacher=teacher,
                        date=lesson_date,
                        end_date=end_date,
                        topic_name=topic_name,
                        lesson_week=lesson_week,
                        lesson_type=lesson_type,
                        lesson_kind=lesson_kind,
                        time_interval=time_interval
                    )
                    lesson_instance.save()
                    lesson_instance.group_number.set(group_numbers)
                    messages.success(request, 'Dərs uğurla əlavə edildi.')
                
                return redirect('add_lesson')
        else:
            messages.error(request, 'Zəhmət olmasa formu düzgün doldurun.')
    else:
        form = LessonForm()

    return render(request, 'add_lesson.html', {'form': form})

def delete_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    lesson.delete()
    return redirect('panel_lessons')

# def update_lesson(request, pk):
#     lesson = Lesson.objects.get(pk=pk)
#     form = LessonForm(instance=lesson)

#     if request.method == 'POST':
#         form = LessonForm(request.POST, instance=lesson)
#         if form.is_valid():
#             new_lesson = form.save(commit=False)
            
#             # 1) Check if there are any lessons on the selected date and time
#             existing_lessons_on_datetime = Lesson.objects.filter(date=new_lesson.date, time_interval=new_lesson.time_interval)
#             if existing_lessons_on_datetime.exists():
#                 # 2) Check if there are lessons in the selected classroom
#                 existing_lessons_in_classroom = existing_lessons_on_datetime.filter(classroom=new_lesson.classroom)
#                 if existing_lessons_in_classroom.exists():
#                     # Exclude the current lesson from the queryset
#                     existing_lessons_in_classroom = existing_lessons_in_classroom.exclude(pk=new_lesson.pk)
#                     if existing_lessons_in_classroom.exists():
#                         # There is a conflict, show error message
#                         messages.error(request, f"Bu saat aralığında seçdiyiniz auditoriyada dərs var!")
#                         return render(request, 'update_lesson.html', {'form': form})
                
#             # 3) Check if the selected teacher has lessons in the same time period.
#             existing_lessons_for_teacher = Lesson.objects.filter(date=new_lesson.date, teacher=new_lesson.teacher, time_interval=new_lesson.time_interval)
#             existing_lessons_for_teacher = existing_lessons_for_teacher.exclude(pk=new_lesson.pk)
#             if existing_lessons_for_teacher.exists():
#                 # There is a conflict, show error message
#                 messages.error(request, "Bu saat aralığında seçdiyiniz müəllimin dərsi var!")
#                 return render(request, 'update_lesson.html', {'form': form})
            
#             # 4) Check if the selected group has lessons in the same time period.
#             # group_numbers_list = [group.group_number for group in new_lesson.group_number.all()]
#             # existing_lessons_for_group = Lesson.objects.filter(date=new_lesson.date, group_number__in=group_numbers_list, time_interval=new_lesson.time_interval)
#             # # existing_lessons_for_group = Lesson.objects.filter(date=new_lesson.date, group_number__in=new_lesson.group_number, time_interval=new_lesson.time_interval)
#             # existing_lessons_for_group = existing_lessons_for_group.exclude(pk=new_lesson.pk)
#             # if existing_lessons_for_group.exists():
#             #     # There is a conflict, show error message
#             #     messages.error(request, "Bu saat aralığında seçdiyiniz qrupun dərsi var!")
#             #     return render(request, 'update_lesson.html', {'form': form})

#             # Yeni dersin grup numaralarını alın
#             for group_number in new_lesson.group_number.all():
#                 existing_lessons_for_group = Lesson.objects.filter(date=new_lesson.date, time_interval=new_lesson.time_interval, group_number=group_number)
#                 existing_lessons_for_group = existing_lessons_for_group.exclude(pk=new_lesson.pk)
#                 print("existing_lessons_for_group:", existing_lessons_for_group)
#                 if existing_lessons_for_group.exists():
#                     messages.error(request, "Bu saat aralığında seçdiyiniz qrupun dərsi var!")
#                     return render(request, 'update_lesson.html', {'form': form})

#             # If there are no conflicts, save the form
#             new_lesson.save()
#             return redirect('panel_lessons')
    
#     context = {
#         'form': form
#     }
#     return render(request, 'update_lesson.html', context)

def update_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    form = LessonForm(instance=lesson)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            
            # 1) Check if there are any lessons on the selected date and time
            existing_lessons_on_datetime = Lesson.objects.filter(date=new_lesson.date, time_interval=new_lesson.time_interval)
            if existing_lessons_on_datetime.exists():
                # 2) Check if there are lessons in the selected classroom
                existing_lessons_in_classroom = existing_lessons_on_datetime.filter(classroom=new_lesson.classroom)
                if existing_lessons_in_classroom.exists():
                    # Exclude the current lesson from the queryset
                    existing_lessons_in_classroom = existing_lessons_in_classroom.exclude(pk=new_lesson.pk)
                    if existing_lessons_in_classroom.exists():
                        # There is a conflict, show error message
                        messages.error(request, f"Bu saat aralığında seçdiyiniz auditoriyada dərs var!")
                        return render(request, 'update_lesson.html', {'form': form})
                
            # 3) Check if the selected teacher has lessons in the same time period.
            existing_lessons_for_teacher = Lesson.objects.filter(date=new_lesson.date, teacher=new_lesson.teacher, time_interval=new_lesson.time_interval)
            existing_lessons_for_teacher = existing_lessons_for_teacher.exclude(pk=new_lesson.pk)
            if existing_lessons_for_teacher.exists():
                # There is a conflict, show error message
                messages.error(request, "Bu saat aralığında seçdiyiniz müəllimin dərsi var!")
                return render(request, 'update_lesson.html', {'form': form})
            
            # Grup numaralarının güncellendiğini kontrol et
            if not set(lesson.group_number.all()) == set(new_lesson.group_number.all()):
                if has_group_conflict(new_lesson):
                    messages.error(request, "Qrup nömrələrini yeniləmək mümkün olmadı.")
                    return render(request, 'update_lesson.html', {'form': form})

            print("Yeni Grup Numaraları:", new_lesson.group_number.all())
            new_lesson.save()
            form.save_m2m()
            return redirect('panel_lessons')
    
    context = {'form': form}
    return render(request, 'update_lesson.html', context)

def has_conflict(new_lesson):
    existing_lessons_on_datetime = Lesson.objects.filter(date=new_lesson.date, time_interval=new_lesson.time_interval)
    if existing_lessons_on_datetime.exists():
        existing_lessons_in_classroom = existing_lessons_on_datetime.filter(classroom=new_lesson.classroom)
        if existing_lessons_in_classroom.exists():
            existing_lessons_in_classroom = existing_lessons_in_classroom.exclude(pk=new_lesson.pk)
            if existing_lessons_in_classroom.exists():
                return True

    existing_lessons_for_teacher = Lesson.objects.filter(date=new_lesson.date, teacher=new_lesson.teacher, time_interval=new_lesson.time_interval)
    existing_lessons_for_teacher = existing_lessons_for_teacher.exclude(pk=new_lesson.pk)
    if existing_lessons_for_teacher.exists():
        return True

    return False

def has_group_conflict(new_lesson):
    for group_number in new_lesson.group_number.all():
        existing_lessons_for_group = Lesson.objects.filter(date=new_lesson.date, time_interval=new_lesson.time_interval, group_number=group_number)
        existing_lessons_for_group = existing_lessons_for_group.exclude(pk=new_lesson.pk)
        print("existing_lessons_for_group:", existing_lessons_for_group)
        if existing_lessons_for_group.exists():
            return True
    return False

def add_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            class_number = form.cleaned_data['class_number']
            all_classrooms = Classroom.objects.all()
            for classroom in all_classrooms:
                if classroom.class_number == class_number:
                    messages.error(request, 'Bu auditoriya nömrəsi artıq mövcuddur!')
                    return redirect('add_classroom')
            form.save()
            messages.success(request, 'Auditoriya uğurla əlavə edildi.')
            return redirect('add_classroom')
    else:
        form = ClassroomForm()
    return render(request, 'add_classroom.html', {'form': form})

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Müəllim uğurla əlavə edildi.')
            return redirect('add_teacher')
    else:
        form = TeacherForm()
    return render(request, 'add_teacher.html', {'form': form})

def add_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Qrup uğurla əlavə edildi.')
            return redirect('add_group')
    else:
        form = GroupForm()
    return render(request, 'add_group.html', {'form': form})

def update_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(instance=teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_panel')
    return render(request, 'update_teacher.html', {'form': form})

def update_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    form = GroupForm(instance=group)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_panel')
    return render(request, 'update_group.html', {'form': form})

def delete_teacher(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    teacher.delete()
    messages.success(request, 'Müəllim uğurla silindi.')
    return redirect('teacher_panel')

def delete_group(request, pk):
    group = Group.objects.get(pk=pk)
    group.delete()
    messages.success(request, 'Qrup uğurla silindi.')
    return redirect('group_panel')

def update_classroom(request, pk):
    classroom = Classroom.objects.get(pk=pk)
    form = ClassroomForm(instance=classroom)
    
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            class_number = form.cleaned_data.get('class_number')
            if Classroom.objects.exclude(pk=pk).filter(class_number=class_number).exists():
                messages.info(request, f'Daxil etdiyiniz auditoriya nömrəsi sistemdə mövcuddur! Zəhmət olmasa yeni auditoriya nömrəsi daxil edin.')
            else:
                form.save()
                return redirect('classroom_panel')
    
    context = {
        'form': form,
    }
    return render(request, 'update_classroom.html', context)

def delete_classroom(request, pk):
    classroom = Classroom.objects.get(pk=pk)
    classroom.delete()
    messages.success(request, 'Auditoriya uğurla silindi.')
    return redirect('classroom_panel')

def teacher_panel(request):
    teachers = Teacher.objects.all()

    query = request.GET.get('q')
    if query:
        teachers = teachers.filter(name__icontains=query)

    return render(request, 'teacher_panel.html', {'teachers': teachers})

def group_panel(request):
    groups = Group.objects.all()

    query = request.GET.get('q')
    if query:
        groups = groups.filter(group_number__icontains=query)

    return render(request, 'group_panel.html', {'groups': groups})

def classroom_panel(request):
    classrooms = Classroom.objects.all()

    query = request.GET.get('q')
    if query:
        classrooms = classrooms.filter(class_number__icontains=query)

    return render(request, 'classroom_panel.html', {'classrooms': classrooms})

def to_roman(number):
    # Convert the number to Roman numeral
    roman_numerals = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'}
    return roman_numerals.get(number, '')

def weekly_limited_filtered_lessons(request):
    now = datetime.now()
    today = now.date()
    show_filter_button = True

    start_date = today - timedelta(days=today.weekday())  # Monday of the current week
    end_date = start_date + timedelta(days=6)  # Sunday of the current week

    if request.method == 'GET':
        if 'refresh' in request.GET:
            return redirect('weekly_only_lessons')
        form = LessonFilterForm(request.GET)
        if form.is_valid():
            # Get filtering options from form
            group_numbers = form.cleaned_data.get('group_number')
            teacher = form.cleaned_data.get('teacher')
            lesson_week = form.cleaned_data.get('lesson_week')
            classroom = form.cleaned_data.get('classroom')
            time_interval = form.cleaned_data['time_interval']
            day_of_week = form.cleaned_data['day_of_week']
            lesson_type = form.cleaned_data.get('lesson_type')
            lesson_kind = form.cleaned_data.get('lesson_kind')

            # Perform filtering operations
            queryset = Lesson.objects.filter(date__range=[start_date, end_date])
            if group_numbers:
                queryset = queryset.filter(group_number__in=group_numbers) 
                # queryset = queryset.filter(Q(group_number__icontains=group_number))

            if teacher:
                queryset = queryset.filter(teacher=teacher)

            if lesson_week:
                queryset = queryset.filter(lesson_week=lesson_week)
                
            if classroom:
                queryset = queryset.filter(classroom=classroom)

            if time_interval:
                queryset = queryset.filter(time_interval=time_interval)
            
            if lesson_type:
                queryset = queryset.filter(lesson_type=lesson_type)

            if lesson_kind:
                queryset = queryset.filter(lesson_kind=lesson_kind)
                    
            days_map = {
                '1': -1,  # Monday
                '2': 0,  # Tuesday
                '3': 1,  # Wednesday
                '4': 2,  # Thursday
                '5': 3,  # Friday
                '6': 4,  # Saturday
                '7': 5,  # Sunday
            }
            if day_of_week in days_map:
                # Find the date of the first day of the week starting from Monday
                weekday = today.weekday()
                diff = weekday - 0  # Indexed as 0 on Monday, 1 on Tuesday, ...
                monday = today - timedelta(days=diff)

                # Find the date of the specified day and filter the courses accordingly
                date_of_selected_day = monday + timedelta(days=days_map[day_of_week])
                queryset = queryset.filter(date=date_of_selected_day)

            # Initialize a dictionary to hold lessons by day
            lessons_by_day = {to_roman(day): [] for day in range(1, 8)}  # Monday is indexed as 1
            
            # Populate the dictionary with lessons grouped by day and sorted by time interval
            for lesson in queryset:
                day_of_week = lesson.date.weekday() + 1  # Adjust indexing for Monday
                roman_day = to_roman(day_of_week)
                lesson_date = lesson.date
                start_time_str, end_time_str = lesson.time_interval.split('-')
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
                
                if lesson_date < today:
                    lesson.is_past = True
                elif lesson_date <= today and (end_time < now.time() or (end_time == now.time() and lesson_date < today)):
                    lesson.is_past = True
                else:
                    lesson.is_past = False

                # Append the lesson to the list of lessons for the corresponding day
                lessons_by_day[roman_day].append(lesson)

            # Sort the lessons within each day by their time intervals
            for day, lessons in lessons_by_day.items():
                lessons_by_day[day] = sorted(lessons, key=lambda x: x.time_interval)
                        
            # Remove days VI and VII from the dictionary if they have no lessons
            if not lessons_by_day.get('VI'):
                del lessons_by_day['VI']

            if not lessons_by_day.get('VII'):
                del lessons_by_day['VII']

            return render(request, 'weekly_only_lessons.html', {'lessons_by_day': lessons_by_day, 'form': form, 'start_date' : start_date, 'end_date' : end_date, 'show_filter_button': show_filter_button})

    else:
        form = LessonFilterForm()
        queryset = Lesson.objects.filter(date__range=[start_date, end_date])
        context = {'lessons_by_day': lessons_by_day, 'form': form, 'show_filter_button': show_filter_button}
        return render(request, 'weekly_only_lessons.html', context)

def table_lessons_filtered_list(request):
    now = datetime.now()
    today = now.date()
    show_filter_button = True

    if request.method == 'GET':
        if 'refresh' in request.GET:
            return redirect('table_only_lessons')
        form = LessonFilterForm(request.GET)
        if form.is_valid():
            # Get filtering options from form
            group_numbers = form.cleaned_data.get('group_number')
            teacher = form.cleaned_data.get('teacher')
            lesson_week = form.cleaned_data.get('lesson_week')
            classroom = form.cleaned_data.get('classroom')
            time_interval = form.cleaned_data.get('time_interval')
            day_of_week = form.cleaned_data.get('day_of_week')
            lesson_type = form.cleaned_data.get('lesson_type')
            lesson_kind = form.cleaned_data.get('lesson_kind')

            # Perform filtering operations
            queryset = Lesson.objects.all()
            if group_numbers:
                queryset = queryset.filter(group_number__in=group_numbers) 
                # queryset = queryset.filter(Q(group_number__icontains=group_number))

            if teacher:
                queryset = queryset.filter(teacher=teacher)

            if lesson_week:
                queryset = queryset.filter(lesson_week=lesson_week)
                
            if classroom:
                queryset = queryset.filter(classroom=classroom)

            if time_interval:
                queryset = queryset.filter(time_interval=time_interval)
            
            if lesson_type:
                queryset = queryset.filter(lesson_type=lesson_type)

            if lesson_kind:
                queryset = queryset.filter(lesson_kind=lesson_kind)

            # Filter by day of week
            if day_of_week:
                queryset = queryset.filter(date__week_day=day_of_week)

            # Sort by date and time_interval in ascending order
            queryset = queryset.order_by('date', F('time_interval').asc())

            # Initialize a dictionary to hold lessons by day
            lessons_by_day = {to_roman(day): [] for day in range(1, 8)}  # Monday is indexed as 1
            
            # Populate the dictionary with lessons grouped by day
            for lesson in queryset:
                day_of_week = lesson.date.weekday() + 1  # Adjust indexing for Monday
                roman_day = to_roman(day_of_week)
                lesson_date = lesson.date
                start_time_str, end_time_str = lesson.time_interval.split('-')
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
                
                if lesson_date < today:
                    lesson.is_past = True
                elif lesson_date <= today and (end_time < now.time() or (end_time == now.time() and lesson_date < today)):
                    lesson.is_past = True
                else:
                    lesson.is_past = False
                
                lessons_by_day[roman_day].append(lesson)
            
            # Remove days VI and VII from the dictionary if they have no lessons
            if not lessons_by_day.get('VI'):
                del lessons_by_day['VI']

            if not lessons_by_day.get('VII'):
                del lessons_by_day['VII']

            return render(request, 'table_only_lessons.html', {'lessons_by_day': lessons_by_day, 'form': form, 'show_filter_button': show_filter_button})

    else:
        form = LessonFilterForm()
        queryset = Lesson.objects.all()
        lessons_by_day = {to_roman(day): [] for day in range(1, 8)}  # Monday is indexed as 1
        
        # Populate the dictionary with lessons grouped by day
        for lesson in queryset:
            day_of_week = lesson.date.weekday() + 1  # Adjust indexing for Monday
            roman_day = to_roman(day_of_week)
            lesson_date = lesson.date
            start_time_str, end_time_str = lesson.time_interval.split('-')
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            if lesson_date < today:
                lesson.is_past = True
            elif lesson_date <= today and (end_time < now.time() or (end_time == now.time() and lesson_date < today)):
                lesson.is_past = True
            else:
                lesson.is_past = False
            
            lessons_by_day[roman_day].append(lesson)

        return render(request, 'table_only_lessons.html', {'lessons_by_day': lessons_by_day, 'form': form, 'show_filter_button': show_filter_button})

def daily_limited_filtered_lessons(request):
    now = datetime.now()
    today = now.date()
    show_filter_button = True

    TIME_INTERVALS = (
        '08:30-09:50',
        '10:00-11:20',
        '11:30-12:50',
        '14:00-15:20',
        '15:30-16:50',
        '17:00-18:20',
    )

    if request.method == 'GET':
        if 'refresh' in request.GET:
            return redirect('daily_only_lessons')
        form = LessonFilterForm(request.GET)
        if form.is_valid():
            # Get filtering options from form
            group_numbers = form.cleaned_data.get('group_number')
            teacher = form.cleaned_data.get('teacher')
            lesson_week = form.cleaned_data.get('lesson_week')
            classroom = form.cleaned_data.get('classroom')
            time_interval = form.cleaned_data.get('time_interval')
            lesson_type = form.cleaned_data.get('lesson_type')
            lesson_kind = form.cleaned_data.get('lesson_kind')


            # Perform filtering operations
            queryset = Lesson.objects.filter(date=today)
            if group_numbers:
                queryset = queryset.filter(group_number__in=group_numbers) 
                # queryset = queryset.filter(group_number=group_number)

            if teacher:
                queryset = queryset.filter(teacher=teacher)

            if lesson_week:
                queryset = queryset.filter(lesson_week=lesson_week)
                
            if classroom:
                queryset = queryset.filter(classroom=classroom)

            if time_interval:
                queryset = queryset.filter(time_interval=time_interval)
            
            if lesson_type:
                queryset = queryset.filter(lesson_type=lesson_type)
            
            if lesson_kind:
                queryset = queryset.filter(lesson_kind=lesson_kind)
            
            lessons_by_time_interval = {interval: [] for interval in TIME_INTERVALS}


            # Populate the dictionary with lessons grouped by day
            for lesson in queryset:
                lesson_date = lesson.date
                start_time_str, end_time_str = lesson.time_interval.split('-')
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
                
                if lesson_date < today:
                        lesson.is_past = True
                elif lesson_date <= today and (end_time < now.time() or (end_time == now.time() and lesson_date < today)):
                    lesson.is_past = True
                else:
                    lesson.is_past = False
                lessons_by_time_interval.setdefault(lesson.time_interval, []).append(lesson)

            return render(request, 'daily_only_lessons.html', {'lessons_by_time_interval': lessons_by_time_interval, 'form': form, 'today': today, 'show_filter_button': show_filter_button})

    else:
        form = LessonFilterForm()
        queryset = Lesson.objects.filter()
        
        # Populate the dictionary with lessons grouped by day
        for lesson in queryset:
            lesson_date = lesson.date
            start_time_str, end_time_str = lesson.time_interval.split('-')
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            if lesson_date < today:
                    lesson.is_past = True
            elif lesson_date <= today and (end_time < now.time() or (end_time == now.time() and lesson_date < today)):
                lesson.is_past = True
            else:
                lesson.is_past = False
            lessons_by_time_interval.setdefault(lesson.time_interval, []).append(lesson)
            
        return render(request, 'daily_only_lessons.html', {'lessons_by_time_interval': lessons_by_time_interval, 'form': form, 'today': today, 'show_filter_button': show_filter_button})

def panel_lessons(request):
    now = datetime.now()
    today = now.date()
    show_filter_button = False

    if request.method == 'GET':
        if 'refresh' in request.GET:
            return redirect('panel_lessons')
        form = LessonFilterForm(request.GET)
        if form.is_valid():
            # Get filtering options from form
            group_number = form.cleaned_data.get('group_number')
            teacher = form.cleaned_data.get('teacher')
            lesson_week = form.cleaned_data.get('lesson_week')
            classroom = form.cleaned_data.get('classroom')
            time_interval = form.cleaned_data.get('time_interval')
            day_of_week = form.cleaned_data.get('day_of_week')
            lesson_type = form.cleaned_data.get('lesson_type')
            lesson_kind = form.cleaned_data.get('lesson_kind')

            # Perform filtering operations
            queryset = Lesson.objects.all()
            if group_number:
                queryset = queryset.filter(group_number=group_number)

            if teacher:
                queryset = queryset.filter(teacher=teacher)

            if lesson_week:
                queryset = queryset.filter(lesson_week=lesson_week)
                
            if classroom:
                queryset = queryset.filter(classroom=classroom)

            if time_interval:
                queryset = queryset.filter(time_interval=time_interval)
            
            if lesson_type:
                queryset = queryset.filter(lesson_type=lesson_type)

            if lesson_kind:
                queryset = queryset.filter(lesson_kind=lesson_kind)

            # Filter by day of week
            if day_of_week:
                queryset = queryset.filter(date__week_day=day_of_week)

            # Sort by date and time_interval in ascending order
            queryset = queryset.order_by('date', F('time_interval').asc())

            # Initialize a dictionary to hold lessons by day
            lessons_by_day = {to_roman(day): [] for day in range(1, 8)}  # Monday is indexed as 1
            
            # Populate the dictionary with lessons grouped by day
            for lesson in queryset:
                day_of_week = lesson.date.weekday() + 1  # Adjust indexing for Monday
                roman_day = to_roman(day_of_week)
                lesson_date = lesson.date
                start_time_str, end_time_str = lesson.time_interval.split('-')
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
                
                if lesson_date < today:
                    lesson.is_past = True
                elif lesson_date <= today and (end_time < now.time() or (end_time == now.time() and lesson_date < today)):
                    lesson.is_past = True
                else:
                    lesson.is_past = False
                
                lessons_by_day[roman_day].append(lesson)

            return render(request, 'panel_lessons.html', {'lessons_by_day': lessons_by_day, 'form': form, 'show_filter_button': show_filter_button})

    else:
        form = LessonFilterForm()
        queryset = Lesson.objects.all()
        lessons_by_day = {to_roman(day): [] for day in range(1, 8)}  # Monday is indexed as 1
        
        # Populate the dictionary with lessons grouped by day
        for lesson in queryset:
            day_of_week = lesson.date.weekday() + 1  # Adjust indexing for Monday
            roman_day = to_roman(day_of_week)
            lesson_date = lesson.date
            start_time_str, end_time_str = lesson.time_interval.split('-')
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            if lesson_date < today:
                lesson.is_past = True
            elif lesson_date <= today and (end_time < now.time() or (end_time == now.time() and lesson_date < today)):
                lesson.is_past = True
            else:
                lesson.is_past = False
            
            lessons_by_day[roman_day].append(lesson)

    return render(request, 'panel_lessons.html', {'lessons_by_day': lessons_by_day, 'show_filter_button': show_filter_button})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('daily_only_lessons')
        else:
            messages.error(request, 'İstifadəçi adı və ya parol səhvdir.')
    return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    return redirect('daily_only_lessons')

def about(request):
    return render(request, 'about.html')

from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit

def generate_pdf(request):
    # Burada gerektiğiniz verileri alarak HTML'i oluşturun
    context = {
        'data': 'Veriler buraya eklenecek',  # İstenilen verileri ekleyin
    }
    html_content = render_to_string('daily_only_lessons.html', context)

    # PDF oluşturucu ayarları
    pdfkit_config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    # PDF oluşturma işlemi
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdf = pdfkit.from_string(html_content, False, options=options, configuration=pdfkit_config)

    # HTTP yanıtı olarak PDF dosyasını gönderin
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'
    return response

import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string

def daily_only_lesson_to_pdf(request):
    # Görünüm fonksiyonu içinde PDF'e dönüştürmek için kullanılacak HTML içeriğini alın
    html_content = render_to_string('daily_only_lessons.html')
    
    # PDF oluşturmak için kullanılacak konfigürasyonu ayarlayın
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    # HTML içeriğini PDF'e dönüştürün
    pdf = pdfkit.from_string(html_content, False, configuration=config)
    
    # HttpResponse nesnesi oluşturun ve PDF içeriğini ekleyin
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="daily_only_lesson.pdf"'
    
    return response