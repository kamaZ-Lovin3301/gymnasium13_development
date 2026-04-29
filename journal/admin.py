from django.contrib import admin
from .models import Teacher, Student, Class, Subject, Schedule, Grade, Homework, Room, TeacherSubject, Parent, ParentStudent

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Schedule)
admin.site.register(Grade)
admin.site.register(Homework)
admin.site.register(Room)
admin.site.register(TeacherSubject)
admin.site.register(Parent)
admin.site.register(ParentStudent)