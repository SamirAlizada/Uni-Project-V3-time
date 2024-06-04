from django import forms
from .models import Lesson, Teacher, Classroom, Group
from django.contrib.admin.widgets import AdminDateWidget


class LessonForm(forms.ModelForm):
    date = forms.DateField(widget=AdminDateWidget)
    end_date = forms.DateField(widget=AdminDateWidget, required=False)

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['group_number'].widget.attrs['class'] = 'form-control'  # Add form control class for group numbers

    class Meta:
        model = Lesson
        fields = ['classroom', 'teacher', 'time_interval', 'date', 'end_date', 'group_number', 'topic_name', 'lesson_week', 'lesson_type', 'lesson_kind']
        labels = {
            'classroom': 'Auditoriya',
            'teacher': 'Müəllim',
            'time_interval': 'Dərs aralığı',
            'date': 'Tarix',
            'end_date': 'Bitiş Tarixi',
            'group_number': 'Qrup nömrəsi',
            'topic_name': 'Dərsin Adı:',
            'lesson_week': 'Dərs həftəsi',
            'lesson_type': 'Dərs Tipi',
            'lesson_kind': 'Dərsin Forması',
        }
        widgets = {
            'classroom': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'time_interval': forms.Select(choices=Lesson.TIME_INTERVALS, attrs={'class': 'form-control'}),
            # 'date': forms.DateInput(format='%d%m%Y', attrs={'class': 'form-control', 'type': 'date'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),
            'topic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson_week': forms.Select(choices=Lesson.LESSON_WEEK_CHOICES, attrs={'class': 'form-control'}),
            'lesson_type': forms.Select(choices=Lesson.LESSON_TYPES, attrs={'class': 'form-control'}),
            'lesson_kind': forms.Select(choices=Lesson.LESSON_KIND, attrs={'class': 'form-control'}),
        }

class LessonFilterForm(forms.Form):
    # group_number = forms.CharField(label='Qrup', required=False)
    group_number = forms.ModelMultipleChoiceField(label='Qrup', queryset=Group.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    # group_number = forms.ModelMultipleChoiceField(label='Qrup', queryset=Group.objects.all(), required=False)
    classroom = forms.ModelChoiceField(label='Sinif', queryset=Classroom.objects.all(), required=False)
    teacher = forms.ModelChoiceField(label='Müəllim', queryset=Teacher.objects.all(), required=False)

    lesson_week = forms.ChoiceField(label='Dərs həftəsi:', required= False, choices=[
        (None, 'Seç'),
        ('Üst', 'Üst'),
        ('Alt', 'Alt'),
    ])

    lesson_type = forms.ChoiceField(label='Dərs tipi: ', required=False, choices = [
        (None, 'Seç'),
        ('adi', 'Adi'),
        ('hibrid', 'Hibrid'),
        ('flip', 'Flip'),
    ])

    lesson_kind = forms.ChoiceField(label='Dərsin forması: ', required=False, choices = [
        (None, 'Seç'),
        ('seminar', 'Seminar'),
        ('mühazirə', 'Mühazirə'),
    ])

    time_interval = forms.ChoiceField(label='Dərs saatı', required=False, choices=[
        ('', 'Seç'),
        ('08:30-09:50', '08:30-09:50'),
        ('10:00-11:20', '10:00-11:20'),
        ('11:30-12:50', '11:30-12:50'),
        ('14:00-15:20', '14:00-15:20'),
        ('15:30-16:50', '15:30-16:50'),
        ('17:00-18:20', '17:00-18:20'),
    ])
    
    DAYS_OF_WEEK = (
        ('', 'Seç'),
        (2, 'Bazar Ertəsi'),
        (3, 'Çərşənbə Axşamı'),
        (4, 'Çərşənbə'),
        (5, 'Cümə Axşamı'),
        (6, 'Cümə'),
        (7, 'Şənbə'),
        (1, 'Bazar'),
    )
    day_of_week = forms.ChoiceField(choices=DAYS_OF_WEEK, label='Həftənin Günü', required=False)

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['class_number', 'is_simple_classroom', 'classroom_network_types', 'class_capacity']
        labels = {
            'class_number': 'Auditoriyanın №',
            'is_simple_classroom': 'Auditoriyanın Tipi',
            'classroom_network_types': 'İnternet',
            'class_capacity': 'Tutum',
        }
        widgets = {
            'class_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_simple_classroom': forms.Select(attrs={'class': 'form-control'}),
            'classroom_network_types': forms.Select(attrs={'class': 'form-control'}),
            'class_capacity': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name']
        labels = {
            'name': 'Müəllimin Adı',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_number']
        labels = {
            'group_number': 'Qrup nömrəsi',
        }
        widgets = {
            'group_number': forms.TextInput(attrs={'class': 'form-control'}),
        }