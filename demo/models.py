from django.db import models
from django.db.models import sql, Q, QuerySet


class SchoolQuery(sql.Query):
    def get_compiler(self, using=None, connection=None, elide_empty=True):
        q = self.clone()
        q_expr = Q(school_id=1)
        q.add_q(q_expr)
        return super(SchoolQuery, q).get_compiler(
            using=using, connection=connection, elide_empty=elide_empty
        )


class SchoolFilterQuerySetMixin:
    def __init__(self, model=None, query=None, using=None, hints=None):
        if query is None and model is not None:
            query = SchoolQuery(model)
        super().__init__(model=model, query=query, using=using, hints=hints)


class ClassroomQuerySet(SchoolFilterQuerySetMixin, QuerySet):
    pass


class ClassroomManager(models.Manager.from_queryset(ClassroomQuerySet)):
    pass


class School(models.Model):
    pass


class Classroom(models.Model):
    school = models.ForeignKey(
        School,
        editable=False,
        on_delete=models.CASCADE
    )
    objects = ClassroomManager()


class Student(models.Model):
    classroom = models.ForeignKey(
        Classroom,
        related_name="student_set",
        on_delete=models.CASCADE,
    )


def demonstrate_bug():
    Student.objects.all().delete()
    Classroom.objects.all().delete()
    School.objects.all().delete()
    school_A = School.objects.create()
    classroom_A = Classroom.objects.create(school=school_A)
    student_A = Student.objects.create(classroom=classroom_A)
    bad_queryset = Classroom.objects.exclude(student_set__id=student_A.id).values("id")
    # Evaluate the queryset to trigger the bug
    len(bad_queryset)