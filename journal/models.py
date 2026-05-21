from django.db import models


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45, db_column='имя', verbose_name='Имя')
    last_name = models.CharField(max_length=45, db_column='фамилия', verbose_name='Фамилия')
    patronymic = models.CharField(max_length=45, db_column='отчество', blank=True, null=True, verbose_name='Отчество')
    email = models.CharField(max_length=100, db_column='электронная_почта', blank=True, null=True,
                             verbose_name='Электронная почта')
    phone = models.CharField(max_length=15, db_column='телефон', blank=True, null=True, verbose_name='Телефон')
    login = models.CharField(max_length=55, db_column='логин', unique=True, verbose_name='Логин')
    password_hash = models.CharField(max_length=256, db_column='пароль_хеш', verbose_name='Пароль (хеш)')
    homeroom_class = models.ForeignKey(
        'Class',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='классный_руководитель_класса_id',
        verbose_name='Класс, в котором учитель является классным руководителем'
    )

    class Meta:
        db_table = 'учитель'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic or ""}'


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_column='название', verbose_name='Название')
    description = models.CharField(max_length=255, db_column='описание', blank=True, null=True, verbose_name='Описание')

    class Meta:
        db_table = 'предмет'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=10, db_column='номер', unique=True, verbose_name='Номер кабинета')
    floor = models.IntegerField(db_column='этаж', blank=True, null=True, verbose_name='Этаж')
    capacity = models.IntegerField(db_column='вместимость', blank=True, null=True, verbose_name='Вместимость')
    description = models.CharField(max_length=255, db_column='описание', blank=True, null=True, verbose_name='Описание')

    class Meta:
        db_table = 'кабинет'
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    def __str__(self):
        return f'Room {self.number}'

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    grade = models.IntegerField(db_column='цифра', verbose_name='Цифра класса')
    letter = models.CharField(max_length=1, db_column='буква', verbose_name='Буква класса')
    academic_year = models.CharField(max_length=9, db_column='учебный_год', blank=True, null=True,
                                     verbose_name='Учебный год')

    class Meta:
        db_table = 'класс'
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    def __str__(self):
        return f'{self.grade}{self.letter}'


class TeacherSubject(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='учитель_id', verbose_name='Учитель')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column='предмет_id', verbose_name='Предмет')

    class Meta:
        db_table = 'учитель_предмет'
        verbose_name = 'Связь учителя и предмета'
        verbose_name_plural = 'Связи учителей и предметов'
        unique_together = ('teacher', 'subject')

    def __str__(self):
        return f'{self.teacher} - {self.subject}'


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='класс_id', verbose_name='Класс')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column='предмет_id', verbose_name='Предмет')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='учитель_id', verbose_name='Учитель')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, db_column='кабинет_id', verbose_name='Кабинет')
    day_of_week = models.IntegerField(db_column='день_недели', verbose_name='День недели (1-пн, 2-вт...)')
    lesson_number = models.IntegerField(db_column='номер_урока', verbose_name='Номер урока')
    start_time = models.TimeField(db_column='время_начала', blank=True, null=True, verbose_name='Время начала')
    end_time = models.TimeField(db_column='время_конца', blank=True, null=True, verbose_name='Время конца')

    class Meta:
        db_table = 'расписание'
        verbose_name = 'Урок в расписании'
        verbose_name_plural = 'Расписание'
        unique_together = ('class_id', 'day_of_week', 'lesson_number')

    def __str__(self):
        return f'{self.class_id} - {self.subject} ({self.teacher})'


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45, db_column='имя', verbose_name='Имя')
    last_name = models.CharField(max_length=45, db_column='фамилия', verbose_name='Фамилия')
    patronymic = models.CharField(max_length=45, db_column='отчество', blank=True, null=True, verbose_name='Отчество')
    birth_date = models.DateField(db_column='дата_рождения', blank=True, null=True, verbose_name='Дата рождения')
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='класс_id', verbose_name='Класс')
    login = models.CharField(max_length=55, db_column='логин', unique=True, verbose_name='Логин')
    password_hash = models.CharField(max_length=256, db_column='пароль_хеш', verbose_name='Пароль (хеш)')

    class Meta:
        db_table = 'ученик'
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=45, db_column='фамилия', verbose_name='Фамилия')
    first_name = models.CharField(max_length=45, db_column='имя', verbose_name='Имя')
    patronymic = models.CharField(max_length=45, db_column='отчество', blank=True, null=True, verbose_name='Отчество')
    login = models.CharField(max_length=55, db_column='логин', unique=True, verbose_name='Логин')
    password_hash = models.CharField(max_length=256, db_column='пароль_хеш', verbose_name='Пароль (хеш)')
    phone = models.CharField(max_length=15, db_column='телефон', blank=True, null=True, verbose_name='Телефон')
    email = models.CharField(max_length=100, db_column='электронная_почта', blank=True, null=True, verbose_name='Электронная почта')

    class Meta:
        db_table = 'родитель'
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic or ""}'


class ParentStudent(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, db_column='родитель_id', verbose_name='Родитель')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='ученик_id', verbose_name='Ученик')

    class Meta:
        db_table = 'родитель_ученик'
        verbose_name = 'Связь родителя и ученика'
        verbose_name_plural = 'Связи родителей и учеников'
        unique_together = ('parent', 'student')

    def __str__(self):
        return f'{self.parent} -> {self.student}'


class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='ученик_id', verbose_name='Ученик')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='расписание_id', verbose_name='Урок')
    grade = models.IntegerField(db_column='оценка', blank=True, null=True, verbose_name='Оценка')
    grade_date = models.DateField(db_column='дата_оценки', verbose_name='Дата оценки')

    class Meta:
        db_table = 'оценка'
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'{self.student} - {self.grade} ({self.grade_date})'


class Homework(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, db_column='расписание_id', verbose_name='Урок')
    description = models.CharField(max_length=255, db_column='описание_задания', verbose_name='Описание задания')
    file = models.FileField(
        upload_to='homework/%Y/%m/%d/',
        blank=True,
        null=True,
        db_column='файл',
        verbose_name='Файл'
    )

    class Meta:
        db_table = 'домашнее_задание'
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

    def __str__(self):
        return f'Homework: {self.description[:50]}...'


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, db_column='заголовок', verbose_name='Заголовок')
    text = models.TextField(db_column='текст', verbose_name='Текст объявления')
    created_at = models.DateTimeField(auto_now_add=True, db_column='дата_создания', verbose_name='Дата создания')
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE, db_column='класс_id', verbose_name='Класс')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='учитель_id', verbose_name='Учитель')

    class Meta:
        db_table = 'объявления'
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

