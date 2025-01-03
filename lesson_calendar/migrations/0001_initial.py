# Generated by Django 4.1.2 on 2024-04-15 14:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('class_number', models.IntegerField()),
                ('is_simple_classroom', models.CharField(choices=[('adi', 'Adi'), ('hibrid', 'Hibrid'), ('laboratoriya', 'Laboratoriya')], default='adi', max_length=20)),
                ('classroom_network_types', models.CharField(choices=[('-', '-'), ('wifi', 'Wifi')], max_length=10, null=True)),
                ('class_capacity', models.IntegerField(default=20)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('topic_name', models.CharField(max_length=100)),
                ('lesson_week', models.CharField(choices=[('Üst', 'Üst'), ('Alt', 'Alt')], default='Üst', max_length=10)),
                ('lesson_type', models.CharField(choices=[('adi', 'Adi'), ('hibrid', 'Hibrid'), ('flip', 'Flip')], default='adi', max_length=10)),
                ('lesson_kind', models.CharField(choices=[('seminar', 'Seminar'), ('mühazirə', 'Mühazirə')], default='seminar', max_length=10)),
                ('time_interval', models.CharField(choices=[('08:30-09:50', '08:30 - 09:50'), ('10:00-11:20', '10:00 - 11:20'), ('11:30-12:50', '11:30 - 12:50'), ('14:00-15:20', '14:00 - 15:20'), ('15:30-16:50', '15:30 - 16:50'), ('17:00-18:20', '17:00 - 18:20')], max_length=11)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson_calendar.classroom')),
                ('group_number', models.ManyToManyField(to='lesson_calendar.group')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson_calendar.teacher')),
            ],
        ),
    ]
