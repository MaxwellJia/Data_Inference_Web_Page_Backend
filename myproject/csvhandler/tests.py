import os
import django
from django.db.models import QuerySet

# Set the Django environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.myproject.settings')  # replace to settings path
django.setup()  # initialize Django evn


from django.test import TestCase
from csvhandler.models import Student

# Create your tests here.
if __name__ == '__main__':
    all_samples: QuerySet[Student] = Student.objects.all()
    samples = Student.objects.filter(gender=1)
    for student in all_samples:
        print(student.name)

    print(all_samples)