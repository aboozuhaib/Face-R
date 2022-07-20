from django.db import models

# Create your models here.


class Attendance(models.Model):
    name = models.CharField(max_length=100, unique=True)
    time = models.CharField(max_length=100, default='ab')

    def __str__(self):
        return self.name


class StudentList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    roll_no = models.IntegerField()
    atndnc = models.BooleanField(default=False)
