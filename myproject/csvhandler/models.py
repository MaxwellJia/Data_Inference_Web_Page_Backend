from django.db import models

# Create your models here.
from django.db import models


class Student(models.Model):
    name = models.TextField(blank=True, null=True)
    birthdate = models.TextField(blank=True, null=True)
    score = models.TextField(blank=True, null=True)
    grade = models.TextField(blank=True, null=True)
    body_height = models.TextField(blank=True, null=True)
    keep_days = models.TextField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    attended = models.TextField(blank=True, null=True)
    complex = models.TextField(blank=True, null=True)
    consultation_timestamp = models.TextField(blank=True, null=True)
    good_field = models.TextField(db_column='Good?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    phone = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sample_data'