from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
from faker import Faker
from models import Student

@require_POST
@csrf_exempt
def generate_student(request):
    fake = Faker()
    student = Student.objects.create(first_name=fake.first_name(), last_name=fake.last_name(), age=fake.random_int(min=18, max=50))
    return HttpResponse(f'Студент, створений с id={student.id}')

@require_GET
def generate_students(request):
    try:
        count = int(request.GET.get('count', 1))
        if count > 100 or count < 1:
            raise ValueError
    except ValueError:
        return HttpResponseBadRequest('Параметр лічильника повинен бути позитивним цілим числом, що не перевищує 100')
    fake = Faker()
    students = [Student(first_name=fake.first_name(), last_name=fake.last_name(), age=fake.random_int(min=18, max=50)) for _ in range(count)]
    Student.objects.bulk_create(students)
    return HttpResponse(f'{count} создано студентів')

