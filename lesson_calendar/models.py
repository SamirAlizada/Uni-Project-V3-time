from django.db import models
from django.utils import timezone

class Classroom(models.Model):
    id = models.IntegerField(primary_key=True)

    class_number = models.IntegerField()
    
    CLASSROOM_TYPES = (
        ('adi', 'Adi'),
        ('hibrid', 'Hibrid'),
        ('laboratoriya', 'Laboratoriya'),
    )
    is_simple_classroom = models.CharField(max_length=20, choices=CLASSROOM_TYPES, default='adi')
    
    CLASSROOM_NETWORK_TYPES = (
        ('-', '-'),
        ('wifi', 'Wifi'),
    )
    classroom_network_types = models.CharField(max_length=10, choices=CLASSROOM_NETWORK_TYPES, null=True)

    class_capacity = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.class_number} - {self.is_simple_classroom} - {self.classroom_network_types} - {self.class_capacity}" 

class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Group(models.Model):
    group_number = models.CharField(max_length=20)

    def __str__(self):
        return self.group_number

class Lesson(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group_number = models.ManyToManyField(Group)
    date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    topic_name = models.CharField(max_length=100)

    LESSON_WEEK_CHOICES = (
        ('Normal', 'Normal'),
        ('Üst', 'Üst'),
        ('Alt', 'Alt'),
    )   
    lesson_week = models.CharField(max_length=10, choices=LESSON_WEEK_CHOICES, default= 'Normal')

    LESSON_TYPES = (
        ('adi', 'Adi'),
        ('hibrid', 'Hibrid'),
        ('flip', 'Flip'),
    )
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPES, default= 'adi')

    LESSON_KIND = (
        ('seminar', 'Seminar'),
        ('mühazirə', 'Mühazirə'),
    )
    lesson_kind = models.CharField(max_length=10, choices=LESSON_KIND, default= 'seminar')

    TIME_INTERVALS = (
    ('08:30-09:50', '08:30 - 09:50'),
    ('10:00-11:20', '10:00 - 11:20'),
    ('11:30-12:50', '11:30 - 12:50'),
    ('14:00-15:20', '14:00 - 15:20'),
    ('15:30-16:50', '15:30 - 16:50'),
    ('17:00-18:20', '17:00 - 18:20'),   
    )
    time_interval = models.CharField(max_length=11, choices=TIME_INTERVALS)

    def __str__(self):
        return f"{self.time_interval} -- {self.teacher} -- {self.group_number} - {self.lesson_week}  - {self.date}"